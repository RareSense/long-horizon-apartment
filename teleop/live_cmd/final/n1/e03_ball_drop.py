zz_b = body_of("r178i1_ball"); zz_sd = "left"; zz_bk = body_of("r186i1_basket")
print("ck", ck_save("n1_ball_at_basket", kind="act", info=dict(note="ball r178 held at the basket stance (AI-operated)")), flush=True)
zz_T = np.array([-5.11, -1.37])
ign_ = tuple(b_ for b_ in INFO["bodies"] if b_ == zz_bk or inside(b_, zz_bk))
mon_start(target=None); MON["held"][zz_sd] = zz_b; MON["last_touch"][zz_sd] = float(d.time); MON["ignore_names"] = ign_
zz_Q = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
def zz_to(z_goal, n=8):
    for k_ in range(n):
        c_ = pad_mid(zz_sd); e_ = zz_T - c_[:2]; dz_ = float(np.clip(z_goal - c_[2], -0.04, 0.04))
        if np.linalg.norm(e_) < 0.015 and abs(z_goal - c_[2]) < 0.015: break
        r_ = thand(zz_sd, dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=dz_, frame="world", Q=zz_Q, tag="ball_to_basket")
        if k_ > 2 and np.linalg.norm(np.asarray(r_["err"])) > 0.03 and abs(r_["grip_pt"][0] - c_[0]) < 0.003: break
try:
    zz_to(0.70, n=10)
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
        PRE_ACTION("squat_follow", dict(h=hh_, l=ll_)); squat_follow((zz_sd,), hh_, ll_, T=1.4)
    zz_to(0.22, n=10)
    print("over", np.round(pad_mid(zz_sd), 3).tolist(), "ball", np.round(centre(zz_b), 3).tolist(), flush=True)
    MON["ignore_names"] = ign_ + (zz_b,)
    PRE_ACTION("open_jaws", {}); open_jaws(zz_sd, T=0.4); MON["held"].pop(zz_sd, None); HELD.pop(zz_sd, None); op.run(1.5)
    hp_ = pad_mid(zz_sd)
    PRE_ACTION("hand_up", {}); servo_pads(zz_sd, hp_[:2], hp_[2] + 0.12, zz_Q, speed=0.06, n=2)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES); op.run(1.0)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("ball", np.round(centre(zz_b), 3).tolist(), "inside", inside(zz_b, zz_bk), "check", item_check("r178i1_ball"), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print(look3("n1_ball_in"), flush=True)
