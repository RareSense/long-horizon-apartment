import time, subprocess, sys
n = int(sys.argv[1]) if len(sys.argv) > 1 else 56
o = ""
for i in range(n):
    o = subprocess.run(["py", "-3.12", r"C:\Users\raresense\sim_wbt\isaac_slot.py", "status"], capture_output=True, text=True).stdout
    if "ISAAC_SLOT.lock': 'home" not in o:
        print("FREE", o)
        break
    time.sleep(10)
else:
    print("HELD", o)
