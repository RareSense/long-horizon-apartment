zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=zz_b)
try:
    Q_ = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
    fwd_ = np.array([np.cos(base()[1]), np.sin(base()[1])])
    for k_ in range(3):
        c_ = centre(zz_b); pm_ = pad_mid(zz_sd)
        ex_ = float((pm_[:2] - c_[:2]) @ fwd_)       # + = pads beyond the ball centre
        aim_ = pad_mid(zz_sd)[:2] - fwd_ * ex_ + 0.0 * fwd_
        tgt_ = ts.ee_pose(zz_sd)[0][:2] - fwd_ * ex_
        PRE_ACTION("servo_pads", {}); e_ = servo_pads(zz_sd, c_[:2] - fwd_ * ex_ * (k_ + 1), 0.765, Q_, speed=0.03, n=2)
        pm2_ = pad_mid(zz_sd)
        print(k_, "pads beyond by", round(ex_, 4), "-> now", round(float((pm2_[:2] - c_[:2]) @ fwd_), 4), "side", round(float((pm2_[:2] - c_[:2]) @ np.array([-fwd_[1], fwd_[0]])), 4), "z", round(float(pm2_[2]), 3), "touch", finger_touch(zz_sd), flush=True)
        if abs(float((pm2_[:2] - c_[:2]) @ fwd_)) < 0.005:
            break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
