exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n2\xlib.py", encoding="utf-8").read())
nm_ = "r195i1_paper"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); SD = "left"; CK_STATE["item"] = "fix_" + nm_
# flat_corners gives a degenerate hull for this crumpled paper (4 points within 2 cm): use its footprint rectangle instead
_fc0 = flat_corners
_r = obj_rect(pb_); _RC = np.array([_r.c + _r.R @ np.array([sx_ * _r.h[0], sy_ * _r.h[1]]) for sx_, sy_ in ((1, 1), (-1, 1), (-1, -1), (1, -1))])
_z = _fc0(pb_)
flat_corners = lambda b_, *a_, **k_: (_RC, _r.c, _z[2], _z[3]) if b_ == pb_ else _fc0(b_, *a_, **k_)
bc_ = centre(bn_)[:2]; G_ = max(_RC, key=lambda c_: np.linalg.norm(c_ - bc_))
st_ = (float(G_[0] + 0.25), float(G_[1] + 0.20), np.pi)
print("rect corners", np.round(_RC, 3).tolist(), "far", np.round(G_, 3).tolist(), "stance", np.round(st_, 3).tolist(), flush=True)
mon_start(target=None)
try:
    walk_tight(st_)
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("at", state(), "corner rel", np.round(rel(np.r_[G_, 0.0]), 3).tolist(), flush=True)
mon_start(target=pb_)
try:
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
        crouch(hh_, ll_, T=1.2)
except Abort as ex_:
    print("squat abort", ex_, flush=True)
MON["on"] = False
c_ = corner_pick(nm_, SD, s_in=0.018, force=8.0); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
flat_corners = _fc0
print("held", HOLD.holding(SD), "paper", np.round(centre(pb_), 3).tolist(), flush=True)
x_report("x09_paper1_pick")
