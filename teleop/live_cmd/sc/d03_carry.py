import time as _tm
MON["on"] = False
_w0 = _tm.time()
zz_b = body_of("r120i1_duck"); zz_cb = body_of("r186i1_basket")
mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
MON["t_max"] = 900.0
try:
    w_ = walk_tight((-4.85, -1.05, np.radians(-125.0)), carry=(SD,))
    print("walk", {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "err_yaw", "why")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False; MON["t_max"] = 240.0
print("state", state(), "fell", fallen(), "duck", np.round(centre(zz_b), 3).tolist(), "held", HOLD.holding(SD), "touch", finger_touch(SD, zz_b), "wall", round(_tm.time() - _w0), flush=True)
print(look3("d03_duck_at_basket"), flush=True)
