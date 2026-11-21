rest_hands(SIDES)
mon_start(target=None)
try:
    w_ = walk_tight((-5.80, -2.20, np.pi))
    print("walk", {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "err_yaw", "way_points")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
except RuntimeError as ex_:
    print("err", str(ex_)[:300], flush=True)
MON["on"] = False
pb_ = body_of("r179i1_toy_pouch")
print("state", state(), "pouch rel", np.round(rel(centre(pb_)), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(pb_)], "touch", contact_report()["body"], "fell", fallen(), flush=True)
print(look3("pouch_stance"), flush=True)
