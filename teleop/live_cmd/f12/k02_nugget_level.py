MON["on"] = False
zz_b = body_of("r93i1_nugget"); SD = "right"; o_ = {}
mon_start(target=zz_b)
try:
    p_, yaw_ = base(); fwd_ = np.array([np.cos(yaw_), np.sin(yaw_)])
    x_ = np.r_[fwd_, 0.0]; y_ = np.array([-fwd_[1], fwd_[0], 0.0]); Rl_ = np.column_stack([x_, y_, np.cross(x_, y_)])
    Q_ = {SD: q_(Rl_)}
    c_ = centre(zz_b); lo_, hi_ = obj_box(zz_b)
    zp_ = float(max(c_[2], lo_[2] + 0.014))
    o_["nugget"] = np.round(c_, 3).tolist(); o_["box_z"] = (round(float(lo_[2]), 3), round(float(hi_[2]), 3))
    open_jaws(SD, T=0.3)
    PRE_ACTION("hand_behind", {}); o_["e_behind"] = np.round(servo_pads(SD, c_[:2] - fwd_ * 0.12, zp_ + 0.03, Q_, speed=0.10), 3).tolist()
    PRE_ACTION("hand_level", {}); o_["e_level"] = np.round(servo_pads(SD, c_[:2] - fwd_ * 0.12, zp_, Q_, speed=0.05), 3).tolist()
    PRE_ACTION("hand_in", {}); o_["e_in"] = np.round(servo_pads(SD, c_[:2], zp_, Q_, speed=0.04), 3).tolist()
    o_["ahead"] = round(ahead_of_pelvis(pad_mid(SD)), 3)
    if np.linalg.norm(o_["e_in"][:2]) < 0.012 and abs(o_["e_in"][2]) < 0.012:
        PRE_ACTION("close_jaws", {}); close_jaws(SD, 6.0, T=0.8)
        g1_ = grip_check(SD, zz_b, min_gap=0.004)
        cc_ = umb_contacts(zz_b); fing_ = {k_[0] for k_ in cc_ if k_[0].startswith(SD + ":")}
        o_["grip"] = {k: g1_[k] for k in g1_ if k in ("ok", "gap", "jaw1_N", "jaw2_N", "between")}; o_["fingers"] = sorted(fing_)
        if g1_["ok"] and len(fing_) == 2:
            hold_on(SD, zz_b); HELD[SD] = dict(min_gap=0.004)
            MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
            z0_ = float(centre(zz_b)[2]); hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.05]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("pull_back", {}); op.move({SD: [hp_[0] - fwd_[0] * 0.12, hp_[1] - fwd_[1] * 0.12, hp_[2]]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
            o_["rose"] = round(float(centre(zz_b)[2]) - z0_, 3); o_["held"] = not hold_lost(SD)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state())
print("NUG", o_, flush=True)
pm_ = pad_mid(SD)
print(close(os.path.join(TELE_DIR, "f12_nugget_grip.jpg"), np.r_[pm_[:2] + np.array([0.3, -0.2]), pm_[2] + 0.2], pm_, "nugget grip"), flush=True)
