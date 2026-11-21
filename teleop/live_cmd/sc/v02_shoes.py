exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
LD = "0642_item_r120i1_duck"; exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\sc\ld.py", encoding="utf-8").read())
for nm_ in ("r105i1_shoe", "r105i2_shoe"):
    ZR = shoe_to_mat(nm_)
    print("RESULT", nm_, {k_: v_ for k_, v_ in ZR.items() if k_ != "route"}, flush=True)
    print("ROUTE", nm_, {k_: v_ for k_, v_ in (ZR.get("route") or {}).items() if k_ in ("ckpt", "done", "pos", "next")}, flush=True)
    if ZR.get("status") != "done":
        break
print(close(os.path.join(LK, "v02_mat_above.jpg"), np.r_[1.66, -1.98, 1.5], np.r_[1.72, -2.05, 0.0], "mat from above"), flush=True)
