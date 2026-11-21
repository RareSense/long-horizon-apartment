MON["on"] = False
ck_save("before_scout_shoes", kind="start")
exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
SH = {}
for nm_ in ("r105i1_shoe", "r105i2_shoe"):
    zz_r = shoe_to_mat(nm_)
    SH[nm_] = zz_r
    b_ = body_of(nm_)
    print("SHOE", nm_, {k_: v_ for k_, v_ in zz_r.items() if k_ in ("status", "why", "wall_s", "look")}, "at", np.round(centre(b_), 3).tolist(), "kit", kit_mem(), flush=True)
    if zz_r.get("status") != "done" or fallen():
        break
print("state", state(), "fell", fallen(), "items", [x for x in ck_list("item")][-3:], flush=True)
