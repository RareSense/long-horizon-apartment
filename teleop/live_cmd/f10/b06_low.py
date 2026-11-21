ck_load(os.path.join(RUN, "checkpoints", "0056_act_push")); gait_on(); op.run(0.3)
zz_b = body_of("r175i1_cardboard_box"); zz_Q = {"left": q_(R_down([1.0, 0.0]))}
zz_X = -5.14; zz_Z = 0.05
mon_start(target=None); MON["ignore_names"] = (zz_b,)
try:
    PRE_ACTION("hand_down", {}); e_ = servo_pads("left", np.array([zz_X, 1.195]), zz_Z, zz_Q, speed=0.04, n=3)
    print("hand", np.round(pad_mid("left"), 3).tolist(), "err", np.round(e_, 3).tolist(), "pads", [np.round(p_, 3).tolist() for p_ in pads("left")], "state", state(), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "box_low"), flush=True)
