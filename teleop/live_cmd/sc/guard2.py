# SCOUT guard (coordinator 20 Nov 15:05, AI-operated): stop OUR Isaac (slot cloth, 47970) when system commit free
# (Win32_OperatingSystem FreeVirtualMemory) < 3.5 GB or our kit.exe private bytes > 16 GB (agreed 15:10). Prints a status line every minute.
import json, os, subprocess, time
PIDF = r"C:\Users\raresense\sim_home\_cloth\_logs\live_47970.pid"
PS = ("$o=Get-CimInstance Win32_OperatingSystem; $p=Get-CimInstance Win32_Process | Select ProcessId,ParentProcessId,Name,PrivatePageCount; "
      "@{free=$o.FreeVirtualMemory; procs=$p} | ConvertTo-Json -Compress -Depth 3")
last = 0
while os.path.exists(PIDF):
    try:
        root = int(open(PIDF).read().strip())
        j = json.loads(subprocess.run(["powershell", "-NoProfile", "-Command", PS], capture_output=True, text=True, timeout=60).stdout)
        free_gb = float(j["free"]) / 1048576.0
        kids, todo = set(), [root]
        P = j["procs"]
        while todo:
            k = todo.pop()
            for x in P:
                if int(x["ParentProcessId"]) == k and int(x["ProcessId"]) not in kids:
                    kids.add(int(x["ProcessId"])); todo.append(int(x["ProcessId"]))
        priv = max([float(x["PrivatePageCount"] or 0) / 1073741824.0 for x in P if int(x["ProcessId"]) in kids and x["Name"].lower() == "kit.exe"] or [0.0])
        if time.time() - last > 60:
            print(time.strftime("%H:%M:%S"), f"commit free {free_gb:.1f} GB, our kit private {priv:.1f} GB", flush=True); last = time.time()
        import shutil as _shg
        cfree = _shg.disk_usage("C:\\").free / 1073741824.0
        if free_gb < 3.5 or priv > 16.0 or cfree < 2.0:
            print(time.strftime("%H:%M:%S"), f"GUARD STOP: commit free {free_gb:.1f} GB, kit private {priv:.1f} GB, C: free {cfree:.1f} GB", flush=True)
            subprocess.run(["py", "-3.12", r"E:\urc_scout\scripts\home\c_live.py", "stop", "47970"])
            break
    except Exception as ex:
        print("guard err", str(ex)[:120], flush=True)
    time.sleep(8)
