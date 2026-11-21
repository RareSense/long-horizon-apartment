nm_ = "r149i1_pouch"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); SD = "right"
mon_start(target=pb_)
try:
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
        crouch(hh_, ll_, T=1.2)
except Abort as ex_:
    print("squat abort", ex_, flush=True)
MON["on"] = False
print("squat", state(), "fell", fallen(), flush=True)
c_ = corner_pick(nm_, SD, s_in=0.018, force=8.0); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
print("held", HOLD.holding(SD), "pouch", np.round(centre(pb_), 3).tolist(), "bin", np.round(centre(bn_), 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
print(look3("x03_pouch_corner"), flush=True)
