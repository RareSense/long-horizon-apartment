exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n2\xlib.py", encoding="utf-8").read())
nm_ = "r195i1_paper"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); SD = "left"; CK_STATE["item"] = "fix_" + nm_
_fc0 = flat_corners
_r = obj_rect(pb_); _RC = np.array([_r.c + _r.R @ np.array([sx_ * _r.h[0], sy_ * _r.h[1]]) for sx_, sy_ in ((1, 1), (-1, 1), (-1, -1), (1, -1))])
_z = _fc0(pb_)
flat_corners = lambda b_, *a_, **k_: (_RC, _r.c, _z[2], _z[3]) if b_ == pb_ else _fc0(b_, *a_, **k_)
print("paper now", np.round(centre(pb_), 3).tolist(), "rect corners", np.round(_RC, 3).tolist(), "state", state(), flush=True)
c_ = corner_pick(nm_, SD, s_in=0.025, force=6.0); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
flat_corners = _fc0
print("held", HOLD.holding(SD), "paper", np.round(centre(pb_), 3).tolist(), flush=True)
x_report("x10_paper1_pick2")
