mon_start(target=None); MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time); MON["t_max"] = 900.0
globals()["CARRY_JOINTS"] = True
try:
    w_ = walk_tight((1.77, -1.80, -np.pi / 2), carry=("right",))
    print("walk", {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "err_yaw", "way_points")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
except RuntimeError as ex_:
    print("err", str(ex_)[:200], flush=True)
finally:
    globals()["CARRY_JOINTS"] = False
MON["on"] = False
print("state", state(), "flat", np.round(centre(zz_b), 3).tolist(), "grip", grip_check("right", zz_b).get("ok"), "touch", contact_report(), "fell", fallen(), flush=True)
print(look3("flat1_at_mat"), flush=True)
