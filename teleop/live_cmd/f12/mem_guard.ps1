# Memory guard for the floor agent's Isaac (slot home, port 47960), AI-operated, 20 Nov:
# stop the session if system commit free < 3.5 GB or this session's kit private > 16 GB (a fresh session already has ~14 GB private) (commit exhaustion killed two sessions).
param([int]$KitPid)
while ($true) {
    $os = Get-CimInstance Win32_OperatingSystem
    $cf = $os.FreeVirtualMemory / 1MB
    $p = Get-Process -Id $KitPid -ErrorAction SilentlyContinue
    if ($null -eq $p) { "kit $KitPid gone"; break }
    $priv = $p.PrivateMemorySize64 / 1GB
    $cfree = (Get-PSDrive C).Free / 1GB
    if ($cf -lt 3.5 -or $priv -gt 16.0 -or $cfree -lt 2.0) {
        "{0} STOP: commit free {1:N2} GB, kit private {2:N2} GB, C: free {3:N2} GB" -f (Get-Date -Format HH:mm:ss), $cf, $priv, $cfree
        & py -3.12 E:\urc_home\scripts\home\h_live.py stop 47960
        break
    }
    Start-Sleep -Seconds 10
}
