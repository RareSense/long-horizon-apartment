zz_b = body_of("r178i1_ball"); zz_sd = "left"; zz_bk = body_of("r186i1_basket")
mon_start(target=None); MON["ignore_names"] = (zz_bk, zz_b, body_of("r187i1_plush"), body_of("r120i2_duck"))
zz_Q = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
try:
    PRE_ACTION("open_jaws", {}); open_jaws(zz_sd, T=0.4); MON["held"].pop(zz_sd, None); HELD.pop(zz_sd, None)
    op.run(1.5)
    print("after open: ball", np.round(centre(zz_b), 3).tolist(), "inside", inside(zz_b, zz_bk), flush=True)
    hp_ = pad_mid(zz_sd)
    PRE_ACTION("hand_up", {}); servo_pads(zz_sd, hp_[:2], hp_[2] + 0.12, zz_Q, speed=0.06, n=2)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); arms_to("rest", [zz_sd], T=1.0)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("ball", np.round(centre(zz_b), 3).tolist(), "inside", inside(zz_b, zz_bk), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), "state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print(close(os.path.join(TELE_DIR, "ball_in.jpg"), np.array([-4.9, -1.0, 1.3]), np.array([-5.18, -1.40, 0.05]), "ball in basket"), flush=True)
