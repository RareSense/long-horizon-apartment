MON["on"] = False
o_ = {}
mon_start(target=zz_b)
try:
    gp2_ = grasp_plan(zz_b, near=RM.rz(base()[1])[:, 1]) or gp_
    g1_ = grip_check(SD, zz_b, min_gap=0.004, at=gp2_["at"])
    cc_ = umb_contacts(zz_b)
    o_["grip_at"] = {k: g1_[k] for k in g1_ if k in ("ok", "gap", "jaw1_N", "jaw2_N", "between", "off_axis")}
    o_["contacts0"] = [(c_[0], c_[2], c_[3]) for c_ in cc_]
    z0_ = float(centre(zz_b)[2])
    o_["lift"] = []
    two_f_ = {c_[0] for c_ in cc_ if c_[0].startswith(SD + ":") and abs(c_[2][2]) < 0.5}
    o_["pinch_ok"] = len(two_f_) == 2 and g1_["jaw1_N"] > 1.5 and g1_["jaw2_N"] > 1.5
    if o_["pinch_ok"]:
        for k_ in range(6):
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", dict(k=k_)); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.035]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            cc_ = umb_contacts(zz_b)
            o_["lift"].append((k_, round(float(centre(zz_b)[2]) - z0_, 3), round(float(pad_mid(SD)[2]), 3), sorted(set(c_[0] for c_ in cc_))))
        cc_ = umb_contacts(zz_b)
        only_fingers_ = bool(cc_) and all(c_[0].startswith(SD + ":") for c_ in cc_)
        g2_ = grip_check(SD, zz_b, min_gap=0.004, at=gp2_["at"])
        o_["after"] = dict(grip={k: g2_[k] for k in g2_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}, only_fingers=only_fingers_, contacts=sorted(set(c_[0] for c_ in cc_)))
        two_f2_ = {c_[0] for c_ in cc_ if c_[0].startswith(SD + ":")}
        if len(two_f2_) == 2 and only_fingers_ and g2_["jaw1_N"] > 0.4 and g2_["jaw2_N"] > 0.4:
            hold_on(SD, zz_b); HELD[SD] = dict(min_gap=0.004, at=gp2_["at"])
            MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
            o_["held"] = True
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state())
print("POUCH", o_, flush=True)
pm_ = pad_mid(SD)
print(close(os.path.join(TELE_DIR, "f12_pouch_lifted.jpg"), np.r_[pm_[:2] + np.array([0.35, 0.25]), pm_[2] + 0.1], np.r_[pm_[:2], pm_[2] - 0.08], "pouch lifted"), flush=True)
