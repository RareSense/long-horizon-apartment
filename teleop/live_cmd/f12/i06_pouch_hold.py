MON["on"] = False
o_ = {}
mon_start(target=zz_b)
try:
    open_jaws(SD, T=0.3)
    p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
    C_, cc0_, zlo_, ztop_ = flat_corners(zz_b); n_c = len(C_)
    k_best = min(range(n_c), key=lambda k: ahead_of_pelvis(C_[k]))
    X_ = C_[k_best]; e1_ = C_[(k_best + 1) % n_c] - X_; e2_ = C_[(k_best - 1) % n_c] - X_
    w_ = e1_ / np.linalg.norm(e1_) + e2_ / np.linalg.norm(e2_); w_ /= np.linalg.norm(w_)
    G_ = X_ + w_ * 0.018
    gp_ = dict(point=np.r_[G_, 0.0], z=float(zlo_ + 0.016), top=float(ztop_))
    o_["corner"] = np.round(X_, 3).tolist(); o_["ahead"] = round(ahead_of_pelvis(G_), 3)
    cd_ = np.r_[-w_[1], w_[0], 0.0]; cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
    Q_ = {SD: q_(R_down(cd_))}
    o_["point"] = np.round(gp_["point"], 3).tolist()
    PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(SD, gp_["point"][:2], gp_["top"] + 0.06, Q_, speed=0.15), 3).tolist()
    PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(SD, gp_["point"][:2], gp_["z"], Q_, speed=0.06), 3).tolist()
    PRE_ACTION("close_jaws", {}); close_jaws(SD, 10.0, T=0.8)
    g1_ = grip_check(SD, None, min_gap=0.004)
    cc_ = umb_contacts(zz_b)
    fing_ = {c_[0] for c_ in cc_ if c_[0].startswith(SD + ":") and abs(c_[2][2]) < 0.5}
    # the robot touches nothing but the pouch (contact_report of robot bodies)
    o_["grip"] = {k: g1_[k] for k in g1_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}; o_["fingers_on_sides"] = sorted(fing_)
    o_["robot_touch"] = contact_report()
    if len(fing_) == 2 and g1_["ok"]:
        hold_on(SD, zz_b); HELD[SD] = dict(min_gap=0.004)
        MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
        z0_ = float(centre(zz_b)[2]); o_["lift"] = []
        for k_ in range(5):
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", dict(k=k_)); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.04]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            cc_ = umb_contacts(zz_b)
            o_["lift"].append((k_, round(float(centre(zz_b)[2]) - z0_, 3), sorted(set(c_[0] for c_ in cc_)), round(HOLD.items[SD]["err"], 4) if SD in HOLD.items else None))
        o_["lost"] = hold_lost(SD)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state())
print("POUCH", o_, flush=True)
pm_ = pad_mid(SD)
print(close(os.path.join(TELE_DIR, "f12_pouch_held.jpg"), np.r_[pm_[:2] + np.array([0.35, 0.25]), pm_[2] + 0.1], np.r_[pm_[:2], pm_[2] - 0.05], "pouch held"), flush=True)
