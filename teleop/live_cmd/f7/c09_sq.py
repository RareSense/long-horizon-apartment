zz_b = body_of("r124i1_sandal")
print("sandal", np.round(centre(zz_b), 3).tolist(), "box h", round(float(obj_box(zz_b)[1][2] - obj_box(zz_b)[0][2]), 3), "spot rf", np.round(bc_to_rf(np.r_[1.449, -2.337, 0.0]), 3).tolist(), flush=True)
mon_start(target=None); MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
try:
    for hh_, ll_ in ((-0.20, 0.35),):
        PRE_ACTION("squat_follow", dict(h=hh_, l=ll_))
        squat_follow(("left",), hh_, ll_, T=1.4)
        print("squat", hh_, state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "fell", fallen(), "held", grip_check("left", zz_b) if "grip_check" in globals() else None, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("look", look_hand("left", "sandal_squat1"), flush=True)
