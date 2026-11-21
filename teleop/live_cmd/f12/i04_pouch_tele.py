exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\u00_helpers.py", encoding="utf-8").read())
MON["on"] = False
zz_b = body_of("r149i1_pouch"); SD = "left"
o_ = {}
mon_start(target=zz_b)
try:
    gp_ = grasp_plan(zz_b)
    h_, ln_ = surface_posture(gp_["z"])
    g_, x_ = surface_stance(gp_["point"], SD, ignore=(zz_b,), squat=h_ < -0.05)
    o_["stance"] = None if g_ is None else np.round(g_, 3).tolist(); o_["posture"] = (h_, ln_)
    hp0_ = pad_mid(SD); servo_pads(SD, hp0_[:2], hp0_[2] + 0.12, {SD: q_(R_down(RM.rz(base()[1])[:, 1]))}, speed=0.1, n=1); rest_hands((SD,), T=0.5)
    if g_ is not None:
        walk_to_stance(g_, zz_b)
    p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
    gp_ = grasp_plan(zz_b, near=lat_) or gp_
    cd_ = max(gp_["closes"], key=lambda c: abs(c @ lat_)); cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
    if h_ < -0.01 or ln_ > 0.01:
        PRE_ACTION("crouch", {}); crouch(h_, ln_, T=1.5)
    Q_ = {SD: q_(R_down(cd_))}
    o_["point"] = np.round(gp_["point"], 3).tolist(); o_["ahead"] = round(ahead_of_pelvis(gp_["point"]), 3)
    open_jaws(SD, T=0.3)
    PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(SD, gp_["point"][:2], gp_["top"] + 0.06, Q_, speed=0.15), 3).tolist()
    PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(SD, gp_["point"][:2], gp_["z"], Q_, speed=0.06), 3).tolist()
    z0_ = float(centre(zz_b)[2])
    PRE_ACTION("close_jaws", {}); close_jaws(SD, 10.0, T=0.8)
    g1_ = grip_check(SD, zz_b, min_gap=0.004)
    o_["grip"] = {k: g1_[k] for k in g1_ if k in ("ok", "gap", "jaw1_N", "jaw2_N", "between")}
    o_["lift"] = []
    if g1_["ok"]:
        for k_ in range(6):
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", dict(k=k_)); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.035]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            cc_ = umb_contacts(zz_b)
            o_["lift"].append((k_, round(float(centre(zz_b)[2]) - z0_, 3), round(float(pad_mid(SD)[2]), 3), sorted(set(c_[0] for c_ in cc_))))
        cc_ = umb_contacts(zz_b)
        only_fingers_ = bool(cc_) and all(c_[0].startswith(SD + ":") for c_ in cc_)
        g2_ = grip_check(SD, zz_b, min_gap=0.004)
        o_["after"] = dict(grip={k: g2_[k] for k in g2_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}, only_fingers=only_fingers_, contacts=[c_[0] for c_ in cc_])
        if g2_["ok"] and only_fingers_:
            hold_on(SD, zz_b); HELD[SD] = dict(min_gap=0.004)
            MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
            o_["held"] = True
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state())
print("POUCH", o_, flush=True)
print(look_grasp(zz_b, SD, "f12_pouch_lifted"), flush=True)
