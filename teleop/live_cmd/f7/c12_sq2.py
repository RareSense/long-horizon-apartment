zz_b = body_of("r124i1_sandal")
mon_start(target=None); MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
try:
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6)):
        PRE_ACTION("squat_follow", dict(h=hh_, l=ll_))
        squat_follow(("left",), hh_, ll_, T=1.4)
        print("squat", hh_, state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "sandal", np.round(centre(zz_b), 3).tolist(), "touch", contact_report(), "fell", fallen(), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
lo_, hi_ = obj_box(zz_b)
print("sandal bottom", round(float(lo_[2]), 3), "pad rf", np.round(bc_to_rf(pad_mid("left")), 3).tolist(), flush=True)
print("look", look_hand("left", "sandal_squat2"), flush=True)
