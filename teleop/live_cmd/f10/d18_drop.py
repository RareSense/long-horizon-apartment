zz_b = body_of("r178i1_ball"); zz_sd = "left"; zz_bk = body_of("r186i1_basket")
zz_T = np.array([-5.11, -1.37])
mon_start(target=None); MON["held"][zz_sd] = zz_b; MON["last_touch"][zz_sd] = float(d.time)
MON["ignore_names"] = (zz_bk, body_of("r187i1_plush"), body_of("r120i2_duck"))
zz_Q = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
def zz_to(z_goal, n=8):
    for k_ in range(n):
        c_ = pad_mid(zz_sd); e_ = zz_T - c_[:2]; dz_ = float(np.clip(z_goal - c_[2], -0.04, 0.04))
        if np.linalg.norm(e_) < 0.015 and abs(z_goal - c_[2]) < 0.015: break
        r_ = thand(zz_sd, dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=dz_, frame="world", Q=zz_Q, tag="ball_to_basket")
        print("mv", r_["grip_pt"], "err", r_["err"], "ball", np.round(centre(zz_b), 3).tolist(), "touch", contact_report()["body"], flush=True)
try:
    zz_to(0.70, n=10)
    print("over basket?", np.round(pad_mid(zz_sd), 3).tolist(), "state", state(), flush=True)
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6)):
        PRE_ACTION("squat_follow", dict(h=hh_, l=ll_)); squat_follow((zz_sd,), hh_, ll_, T=1.4)
        print("squat", state()["pelvis"], "pad", np.round(pad_mid(zz_sd), 3).tolist(), "touch", contact_report()["body"], flush=True)
    zz_to(0.26, n=12)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("ball", np.round(centre(zz_b), 3).tolist(), "basket", [np.round(v_, 3).tolist() for v_ in obj_box(zz_bk)], "pad", np.round(pad_mid(zz_sd), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print(look_hand(zz_sd, "ball_over_basket"), flush=True)
