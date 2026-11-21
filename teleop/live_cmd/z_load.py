for _f in ("route_v3_setup.py", "teleop.py", "autorun.py", "aside.py", "ops.py"):
    exec(open(r"E:\urc_home\scripts\home\live\\" + _f, encoding="utf-8").read())
zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece")
TUCK_JOINTS = False
STANCE_LOW_ROOM = 0.35
STANCE_FUR_ROOM = 0.32
print("resumed", str(zz_m)[:300])
print("route pos", POS, "done", len(DONE), "next", [item_name(s_) for s_ in ROUTE[POS:POS + 6]])
print(state(), kit_mem())
zz_sp = scooter_parts("r126i1_scooter")
print("r126 bar_c", np.round(zz_sp["bar_c"], 3), "axis", np.round(zz_sp["bar_axis"], 2), "half", round(zz_sp["bar_half"], 3), "stem", np.round(zz_sp["stem"], 3), "deck", np.round(zz_sp["deck"], 2), "com", np.round(zz_sp["com"], 3))
print("r126 box", [np.round(v_, 3).tolist() for v_ in obj_box("r126i1_scooter")])
print("r127 box", [np.round(v_, 3).tolist() for v_ in obj_box("r127i1_scooter")])
