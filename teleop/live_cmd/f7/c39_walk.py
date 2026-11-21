mon_start(target=None); MON["t_max"] = 900.0; MON["trace"] = []
zz_o = {}
try:
    back_off_container()
    zz_w = walk_tight((-5.28, -0.767, -1.414))
    zz_o = {k_: v_ for k_, v_ in zz_w.items() if k_ in ("err_xy", "err_yaw", "ok", "way_points")} if isinstance(zz_w, dict) else zz_w
except Abort as ex_:
    zz_o = dict(abort=str(ex_))
except RuntimeError as ex_:
    zz_o = dict(error=str(ex_)[:300])
MON["on"] = False
print("WALK", zz_o, flush=True)
print("trace", MON["trace"][::6], flush=True)
print("state", state(), "touch", contact_report(), "fell", fallen(), "kit", kit_mem(), flush=True)
print("look", look3("toy_corner_entry"), flush=True)
