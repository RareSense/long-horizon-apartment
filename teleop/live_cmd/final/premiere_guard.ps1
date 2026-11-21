# Machine-level guard (20 Nov, user rule): when memory gets tight, close Premiere / Media Encoder,
# never the Isaac Sim recording or render. Acts BEFORE the Isaac guards (those stop at commit free < 3.5 GB).
# Thresholds: commit free < 7 GB or available RAM < 3 GB -> stop Premiere-family processes.
$log = "C:\Users\raresense\sim_home\apartment\live_cmd\final\premiere_guard.log"
$names = @("Adobe Premiere Pro", "Adobe Media Encoder", "Dynamic Link Manager", "dynamiclinkmanager", "PProHeadless", "CEPHtmlEngine")
"$(Get-Date -f s) premiere_guard started" | Out-File -Append -Encoding utf8 $log
while ($true) {
    try {
        $os = Get-CimInstance Win32_OperatingSystem
        $commit = $os.FreeVirtualMemory / 1MB
        $ram = $os.FreePhysicalMemory / 1MB
        if ($commit -lt 7 -or $ram -lt 3) {
            $p = Get-Process -ErrorAction SilentlyContinue | Where-Object { $names -contains $_.ProcessName }
            if ($p) {
                foreach ($x in $p) {
                    "$(Get-Date -f s) commit {0:N1} GB, RAM {1:N1} GB -> closing {2} ({3})" -f $commit, $ram, $x.ProcessName, $x.Id | Out-File -Append -Encoding utf8 $log
                    try { $x.CloseMainWindow() | Out-Null } catch {}
                }
                Start-Sleep -Seconds 8
                Get-Process -ErrorAction SilentlyContinue | Where-Object { $names -contains $_.ProcessName } | Stop-Process -Force -ErrorAction SilentlyContinue
            }
        }
    } catch {}
    Start-Sleep -Seconds 3
}
