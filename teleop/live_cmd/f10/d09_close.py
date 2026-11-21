zz_b = body_of("r178i1_ball"); zz_sd = "left"
mon_start(target=zz_b)
zz_out = {}
try:
    Q_ = {zz_sd: q_(ts.ee_pose(zz_sd)[1])}
    z0_ = float(centre(zz_b)[2])
    PRE_ACTION("close_jaws", {}); close_jaws(zz_sd, 12.0, T=0.8)
    g1_ = grip_check(zz_sd, zz_b, min_gap=0.004); zz_out["g1"] = {k_: g1_.get(k_) for k_ in ("ok", "gap", "jaw1_N", "jaw2_N")}
    print("grip", g1_, flush=True)
    if g1_["ok"]:
        hp_ = ts.ee_pose(zz_sd)[0]
        PRE_ACTION("lift", {}); op.move({zz_sd: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
        rose_ = float(centre(zz_b)[2] - z0_); g2_ = grip_check(zz_sd, zz_b, min_gap=0.004)
        zz_out.update(rose=round(rose_, 3), g2=g2_.get("ok"))
        if g2_["ok"] and rose_ > 0.04:
            hold_on(zz_sd, zz_b); HELD[zz_sd] = dict(min_gap=0.004)
            MON["held"][zz_sd] = zz_b; MON["target"] = None; MON["last_touch"][zz_sd] = float(d.time)
            z_c = float(np.clip(z0_ - (centre(zz_b)[2] - obj_box(zz_b)[0][2]) + (pad_mid(zz_sd)[2] - obj_box(zz_b)[0][2]) + 0.08, 0.72 + H_WALK, 0.95))
            PRE_ACTION("carry_pose", {}); carry_pose(zz_sd, z=z_c)
            PRE_ACTION("crouch_holding", {}); crouch_holding((zz_sd,), H_WALK, 0.0, T=2.5)
            zz_out["g3"] = grip_check(zz_sd, zz_b, min_gap=0.004).get("ok")
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "ball", np.round(centre(zz_b), 3).tolist(), "state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
print(look_hand(zz_sd, "ball_held"), flush=True)
