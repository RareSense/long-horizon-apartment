zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=zz_b)
try:
    gp_ = grasp_plan(zz_b, near=RM.rz(base()[1])[:, 1])
    Q_ = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
    print("pads", [np.round(p_, 3).tolist() for p_ in pads(zz_sd)], "ball", np.round(centre(zz_b), 3).tolist(), "finger touch", finger_touch(zz_sd), flush=True)
    for k_ in range(3):
        PRE_ACTION("servo_pads", {}); e_ = servo_pads(zz_sd, gp_["point"][:2], gp_["z"], Q_, speed=0.03, n=2)
        print(k_, "e", np.round(e_, 4).tolist(), "pad mid", np.round(pad_mid(zz_sd), 3).tolist(), "ee", np.round(ts.ee_pose(zz_sd)[0], 3).tolist(), "touch", finger_touch(zz_sd), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
