# Memory guard for the FINAL clean recorded episode (slot home, port 47960), AI-operated, 20 Nov.
# Watches the REAL kit.exe pid (not h_live's cmd.exe wrapper). Stops the session when: system commit free < 3.5 GB,
# kit private > 16 GB, available RAM < 2.5 GB, or C: free < 2 GB. Writes one line every 30 s to guard.log
# (and "RESTART_SOON" once private passes 15 GB: restart fresh at the next item checkpoint).
param([int]$KitPid)
$log = "C:\Users\raresense\sim_home\apartment\live_cmd\final\guard2.log"
$i = 0
while ($true) {
    $os = Get-CimInstance Win32_OperatingSystem
    $cf = $os.FreeVirtualMemory / 1MB
    $av = $os.FreePhysicalMemory / 1MB
    $p = Get-Process -Id $KitPid -ErrorAction SilentlyContinue
    if ($null -eq $p) { "{0} kit {1} gone" -f (Get-Date -Format HH:mm:ss), $KitPid | Add-Content $log; break }
    $priv = $p.PrivateMemorySize64 / 1GB
    $cfree = (Get-PSDrive C).Free / 1GB
    $line = "{0} kit {1} private {2:N2} GB, commit free {3:N2} GB, avail RAM {4:N2} GB, C: free {5:N2} GB" -f (Get-Date -Format HH:mm:ss), $KitPid, $priv, $cf, $av, $cfree
    if ($cf -lt 3.5 -or $priv -gt 16.0 -or $av -lt 2.5 -or $cfree -lt 2.0) {
        "STOP " + $line | Add-Content $log
        & py -3.12 E:\urc_final\scripts\home\h_live.py stop 47960
        break
    }
    if ($priv -gt 15.0) { $line = "RESTART_SOON " + $line }
    if (($i % 3) -eq 0 -or $priv -gt 15.0) { $line | Add-Content $log }
    $i++
    Start-Sleep -Seconds 10
}
