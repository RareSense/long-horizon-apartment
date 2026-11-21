# Guard for the final-look live session (slot "cloth", port 47970). AI-operated.
# Stops OUR Isaac only (c_live.py stop) if: commit free < 3.5 GB, our kit private > 16 GB, available RAM < 2.5 GB,
# or C: free < 2 GB. Exits when our pid file disappears.
import os, sys, time, shutil, subprocess, psutil
sys.path.insert(0, r"C:\Users\raresense\sim_wbt")
import isaac_slot
PIDF = r"C:\Users\raresense\sim_home\_cloth\_logs\live_47970.pid"
LOG = r"C:\Users\raresense\sim_home\apartment\final_look_v6\cmd\guard.log"


def kit_private(pid):
    try:
        root = psutil.Process(pid)
        return max([p.memory_info().private for p in [root] + root.children(recursive=True)] or [0]) / 2 ** 30
    except Exception:
        return 0.0


def log(s):
    open(LOG, "a").write(time.strftime("%H:%M:%S ") + s + "\n")


log("guard start")
last = 0
while os.path.exists(PIDF):
    try:
        pid = int(open(PIDF).read().strip())
    except Exception:
        time.sleep(2); continue
    av, cf = isaac_slot.ram(); kp = kit_private(pid); cfree = shutil.disk_usage("C:\\").free / 2 ** 30
    why = None
    if cf < 3.5: why = f"commit free {cf:.1f} GB"
    elif kp > 16: why = f"kit private {kp:.1f} GB"
    elif av < 2.5: why = f"available RAM {av:.1f} GB"
    elif cfree < 2: why = f"C: free {cfree:.1f} GB"
    if time.time() - last > 60:
        last = time.time(); log(f"RAM {av:.1f} commit {cf:.1f} kit {kp:.1f} C: {cfree:.1f}")
    if why:
        log("STOP: " + why)
        subprocess.run(["py", "-3.12", r"E:\urc_look\scripts\home\c_live.py", "stop", "47970"])
        break
    time.sleep(3)
log("guard end")
