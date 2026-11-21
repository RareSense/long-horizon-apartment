exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\u00_helpers.py", encoding="utf-8").read())
MON["on"] = False
zz_b = body_of("r87i1_wrapper"); o_ = {}
mon_start(target=zz_b)
try:
    o_["walk"] = "none (already at the counter)"
    p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
    gp_ = grasp_plan(zz_b, near=lat_) or grasp_plan(zz_b)
    opts_ = (gp_.get("options") or [gp_])
    gp_ = min(opts_, key=lambda o: ahead_of_pelvis(o["point"]))
    SD = "left" if (gp_["point"][:2] - p_[:2]) @ lat_[:2] > 0 else "right"
    cd_ = max(gp_["closes"], key=lambda c: abs(c @ lat_)); cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
    Q_ = {SD: q_(R_down(cd_))}
    h_, ln_ = surface_posture(gp_["z"]); ln_ = max(ln_, 0.35)
    o_.update(side=SD, point=np.round(gp_["point"], 3).tolist(), ahead=round(ahead_of_pelvis(gp_["point"]), 3), posture=(h_, ln_), width=round(float(gp_.get("width", 0)), 3))
    open_jaws(SD, T=0.2)
    if h_ < -0.01 or ln_ > 0.01:
        PRE_ACTION("crouch", {}); crouch(h_, ln_, T=1.5)
    PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(SD, gp_["point"][:2], gp_["top"] + 0.06, Q_, speed=0.15), 3).tolist()
    PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(SD, gp_["point"][:2], gp_["z"], Q_, speed=0.06), 3).tolist()
    if np.linalg.norm(o_["e_down"]) < 0.015:
        PRE_ACTION("close_jaws", {}); close_jaws(SD, 10.0, T=0.8)
        g1_ = grip_check(SD, None, min_gap=0.0015)
        cc_ = umb_contacts(zz_b)
        fing_ = {c_[0] for c_ in cc_ if c_[0].startswith(SD + ":")}
        o_["grip"] = {k: g1_[k] for k in g1_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}; o_["fingers"] = sorted(fing_)
        if len(fing_) == 2 and g1_["ok"]:
            hold_on(SD, zz_b); HELD[SD] = dict(min_gap=0.0015)
            MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
            z0_ = float(centre(zz_b)[2])
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.06, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            o_["rose"] = round(float(centre(zz_b)[2]) - z0_, 3)
            o_["held"] = not hold_lost(SD)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state())
print("WRAP", o_, flush=True)
print(look3("f12_wrapper_pick"), flush=True)
