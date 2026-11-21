zz_b = body_of("r175i1_cardboard_box"); zz_Q = {"left": q_(R_down([1.0, 0.0]))}
mon_start(target=None); MON["ignore_names"] = (zz_b,)
try:
    hp_ = pad_mid("left")
    PRE_ACTION("hand_back", {}); servo_pads("left", np.array([hp_[0], hp_[1] - 0.05]), hp_[2] + 0.02, zz_Q, speed=0.04, n=2)
    PRE_ACTION("hand_up", {}); servo_pads("left", np.array([hp_[0], hp_[1] - 0.06]), 0.30, zz_Q, speed=0.08, n=2)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2)
    arms_to("rest", ["left"], T=1.0)
    print("stood", state(), "box", np.round(centre(zz_b), 3).tolist(), "touch", contact_report()["body"], flush=True)
    r_ = tmove(fwd=0.08, tag="box_step_fwd")
    print("step", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
        PRE_ACTION("squat", dict(h=hh_, l=ll_)); crouch(hh_, ll_, T=1.2)
    lo_, hi_ = obj_box(zz_b)
    PRE_ACTION("hand_above", {}); servo_pads("left", np.array([-5.14, lo_[1] - 0.05]), 0.30, zz_Q, speed=0.10, n=2)
    PRE_ACTION("hand_down", {}); e_ = servo_pads("left", np.array([-5.14, lo_[1] - 0.04]), 0.05, zz_Q, speed=0.05, n=3)
    print("hand", np.round(pad_mid("left"), 3).tolist(), "err", np.round(e_, 3).tolist(), "state", state(), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "box_low2"), flush=True)
