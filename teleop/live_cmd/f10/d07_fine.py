zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=zz_b)
try:
    Q_ = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
    print("geom 26", m.geom(26).name, m.body(int(m.geom_bodyid[26])).name, flush=True)
    for zz_z in (0.765, 0.762):
        c_ = centre(zz_b)
        PRE_ACTION("servo_pads", {}); e_ = servo_pads(zz_sd, c_[:2], zz_z, Q_, speed=0.03, n=3)
        print(zz_z, "e", np.round(e_, 4).tolist(), "pads", [np.round(p_, 3).tolist() for p_ in pads(zz_sd)], "ball", np.round(centre(zz_b), 3).tolist(), "touch", finger_touch(zz_sd), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand(zz_sd, "ball_fine"), flush=True)
