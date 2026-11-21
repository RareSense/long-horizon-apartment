# push the cardboard box north with the closed left jaws (fingers down), the robot standing still east-south of it facing north
zz_b = body_of("r175i1_cardboard_box")
zz_X = globals().get("ZZ_X", -5.14)     # push line (x) on the box's south face
zz_Z = globals().get("ZZ_Z", 0.11)      # pad middle height while pushing
zz_Y_GOAL = 1.56
zz_Q = {"left": q_(R_down([1.0, 0.0]))}
mon_start(target=None); MON["ignore_names"] = (zz_b,)
zz_log = []
try:
    PRE_ACTION("close_jaws", dict(side="left")); close_jaws("left", 10.0, T=0.6)
    for hh_, ll_ in ZZ_POSE:
        PRE_ACTION("squat", dict(h=hh_, l=ll_)); crouch(hh_, ll_, T=1.2)
    lo_, hi_ = obj_box(zz_b)
    PRE_ACTION("hand_above", {}); e1_ = servo_pads("left", np.array([zz_X, lo_[1] - 0.05]), 0.32, zz_Q, speed=0.10, n=2)
    PRE_ACTION("hand_down", {}); e2_ = servo_pads("left", np.array([zz_X, lo_[1] - 0.04]), zz_Z, zz_Q, speed=0.05, n=3)
    print("hand at", np.round(pad_mid("left"), 3).tolist(), "err", np.round(e2_, 3).tolist(), "state", state(), "touch", contact_report()["body"], flush=True)
    print(look_hand("left", "box_hand_down"), flush=True)
    if ZZ_PUSH:
        for k_ in range(14):
            c_ = centre(zz_b)
            if c_[1] >= zz_Y_GOAL - 0.005:
                break
            hp_ = pad_mid("left")
            PRE_ACTION("push", dict(k=k_))
            servo_pads("left", np.array([zz_X, hp_[1] + 0.03]), zz_Z, zz_Q, speed=0.04, n=2)
            c2_ = centre(zz_b)
            zz_log.append((k_, np.round(pad_mid("left"), 3).tolist(), np.round(c2_, 3).tolist(), round(float(np.degrees(np.arctan2(d.xmat[m.body(zz_b).id][3], d.xmat[m.body(zz_b).id][0]))), 1)))
            print("push", zz_log[-1], "touch", contact_report()["body"], flush=True)
            if c2_[1] - c_[1] < 0.004 and k_ > 2:
                print("box no longer moves", flush=True)
                break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("box", np.round(centre(zz_b), 3).tolist(), "box lims", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
print(look_hand("left", "box_pushed"), flush=True)
