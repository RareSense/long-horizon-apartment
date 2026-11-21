_start_item("r178i1_ball")
zz_b = body_of("r178i1_ball"); zz_sd = "left"; zz_out = {}
mon_start(target=zz_b)
try:
    w_ = walk_tight((-5.80, -2.13, np.pi))
    zz_out["walk"] = {k_: w_.get(k_) for k_ in ("ok", "err_xy")} if isinstance(w_, dict) else str(w_)[:100]
except (Abort, RuntimeError) as ex_:
    zz_out["walk_abort"] = str(ex_)[:200]
MON["on"] = False
print("WALK", zz_out, state(), "ball rel", np.round(rel(centre(zz_b)), 3).tolist(), flush=True)
if "walk_abort" not in zz_out:
    print("ck", ck_save("n1_ball_stance", kind="act", info=dict(note="sill stance for ball r178 (AI-operated)")), flush=True)
    mon_start(target=zz_b)
    try:
        p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
        gp_ = grasp_plan(zz_b, near=lat_) or grasp_plan(zz_b)
        cd_ = max(gp_["closes"], key=lambda c: abs(c @ lat_)) if gp_["closes"] else lat_
        cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
        Q_ = {zz_sd: q_(R_down(cd_))}
        open_jaws(zz_sd, T=0.2)
        PRE_ACTION("crouch", {}); crouch(0.0, 0.3, T=1.5)
        PRE_ACTION("servo_pads", {}); e1_ = servo_pads(zz_sd, gp_["point"][:2], gp_["top"] + 0.06, Q_, speed=0.2)
        fwd_ = np.array([np.cos(base()[1]), np.sin(base()[1])])
        for k_ in range(4):
            c_ = centre(zz_b); pm_ = pad_mid(zz_sd); ex_ = float((pm_[:2] - c_[:2]) @ fwd_)
            PRE_ACTION("servo_pads", {}); e_ = servo_pads(zz_sd, c_[:2] - fwd_ * ex_ * (k_ + 1) if k_ else c_[:2], 0.765, Q_, speed=0.04, n=2)
            pm2_ = pad_mid(zz_sd)
            zz_out[f"s{k_}"] = (round(float((pm2_[:2] - c_[:2]) @ fwd_), 4), round(float((pm2_[:2] - c_[:2]) @ np.array([-fwd_[1], fwd_[0]])), 4), round(float(pm2_[2]), 3))
            if abs(zz_out[f"s{k_}"][0]) < 0.005 and abs(zz_out[f"s{k_}"][1]) < 0.006:
                break
        z0_ = float(centre(zz_b)[2])
        PRE_ACTION("close_jaws", {}); close_jaws(zz_sd, 12.0, T=0.8)
        g1_ = grip_check(zz_sd, zz_b, min_gap=0.004); zz_out["g1"] = {k_: g1_.get(k_) for k_ in ("ok", "gap", "jaw1_N", "jaw2_N")}
        if g1_["ok"]:
            hp_ = ts.ee_pose(zz_sd)[0]
            PRE_ACTION("lift", {}); op.move({zz_sd: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
            rose_ = float(centre(zz_b)[2] - z0_); g2_ = grip_check(zz_sd, zz_b, min_gap=0.004)
            zz_out.update(rose=round(rose_, 3), g2=g2_.get("ok"), fingers=len(jaw_fingers_on(zz_sd, zz_b)))
            if g2_["ok"] and rose_ > 0.04 and hold_on(zz_sd, zz_b):
                HELD[zz_sd] = dict(min_gap=0.004); MON["held"][zz_sd] = zz_b; MON["target"] = None; MON["last_touch"][zz_sd] = float(d.time)
                zz_out["held"] = True
    except Abort as ex_:
        zz_out["abort"] = str(ex_)
    MON["on"] = False
print("OUT", zz_out, "ball", np.round(centre(zz_b), 3).tolist(), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print(look_hand(zz_sd, "n1_ball_take"), flush=True)
