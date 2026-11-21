zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=None); MON["held"][zz_sd] = zz_b; MON["last_touch"][zz_sd] = float(d.time); MON["t_max"] = 900.0
globals()["CARRY_JOINTS"] = True
try:
    w_ = walk_tight((-5.246, -0.984, -1.414), carry=(zz_sd,))
    print("walk", {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "err_yaw", "way_points")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
except RuntimeError as ex_:
    print("err", str(ex_)[:300], flush=True)
finally:
    globals()["CARRY_JOINTS"] = False
MON["on"] = False
bb_ = body_of("r186i1_basket")
print("state", state(), "ball", np.round(centre(zz_b), 3).tolist(), "grip", grip_check(zz_sd, zz_b).get("ok"), "basket", [np.round(v_, 3).tolist() for v_ in obj_box(bb_)], "rel", np.round(rel(centre(bb_)), 3).tolist(), "touch", contact_report(), "fell", fallen(), flush=True)
print(look3("ball_at_basket"), flush=True)
