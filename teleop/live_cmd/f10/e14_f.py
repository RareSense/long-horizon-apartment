exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
print("forces", {s_: zz_force(s_) for s_ in SIDES}, "finger_touch", finger_touch("left"), finger_touch("right"), "pid", pid_, flush=True)
