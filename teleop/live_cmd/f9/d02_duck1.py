exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f9\zz_pick_here.py", encoding="utf-8").read())
mon_start(target=zz_b)
zz_o = {}
try:
    w_ = walk_tight((1.775, -1.841, np.pi / 2))
    zz_o["turn"] = (state()["pelvis"], state()["yaw_deg"])
    print("reach", in_reach(grasp_plan(zz_b)["point"], "right"), flush=True)
    zz_o["pick"] = zz_pick_here(zz_b, "right")
except Abort as ex_:
    zz_o["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_o["error"] = str(ex_)[:200]
MON["on"] = False
print("OUT", zz_o, "state", state(), "touch", contact_report(), flush=True)
