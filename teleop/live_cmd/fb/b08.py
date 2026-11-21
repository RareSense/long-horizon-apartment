exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\zz_pin.py", encoding="utf-8").read())
for zz_k in range(ZZ_N):
    zz_r = zz_step_to(zz_o, 994, zz_QL, maxs=0.04)
    print("step", zz_k, zz_r, flush=True)
    if zz_r["left"] < 0.008 or fallen():
        break
print("look", zz_look(pad_mid(zz_o), "left_approach", dist=0.7, h=0.25, dirs=(120.0, 30.0, 75.0), top=True), flush=True)
