# Zero-token watcher: exits (waking the coordinator) only when the no-AI runner is done, stopped, or stalled.
$a = 'C:\Users\raresense\sim_home\apartment'
while ($true) {
    if (Test-Path "$a\RUN_DONE.txt") { 'RUN_DONE'; Get-Content "$a\RUN_DONE.txt"; break }
    if ((Test-Path "$a\RUN_NEEDS_AI.txt") -and (Select-String -Path "$a\RUN_NEEDS_AI.txt" -Pattern 'STOP' -Quiet)) {
        'RUNNER_STOPPED'; Get-Content "$a\RUN_NEEDS_AI.txt" -Tail 5; break }
    $l = Get-Item "$a\final_runner.log" -ErrorAction SilentlyContinue
    if ($l -and ((Get-Date) - $l.LastWriteTime).TotalMinutes -gt 50) { 'RUNNER_STALLED'; Get-Content "$a\final_runner.log" -Tail 5; break }
    Start-Sleep 120
}
