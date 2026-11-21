zz_b = body_of("r124i1_sandal")
zz_Q = {"left": q_(ts.ee_pose("left")[1])}
try:
    PRE_ACTION("squat_follow", dict(h=-0.38, l=0.8))
    squat_follow(("left",), -0.38, 0.8, T=1.4)
    print("squat", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "bottom", round(float(obj_box(zz_b)[0][2]), 3), "touch", contact_report(), "fell", fallen(), flush=True)
    for k_ in range(4):
        lo_ = float(obj_box(zz_b)[0][2])
        if lo_ < 0.025:
            break
        dz_ = -min(0.04, lo_ - 0.015)
        PRE_ACTION("bc_hand", dict(side="left", dz=dz_))
        bc_pads_to("left", pad_mid("left") + np.array([0, 0, dz_]), Q=zz_Q, speed=0.04, step=0.04)
        print("down", k_, "bottom", round(float(obj_box(zz_b)[0][2]), 3), "touch", contact_report(), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
print("pad rf", np.round(bc_to_rf(pad_mid("left")), 3).tolist(), "sandal", np.round(centre(zz_b), 3).tolist(), flush=True)
print("look", look_hand("left", "sandal_low2"), flush=True)
