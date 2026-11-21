def corner_pick(nm, side, s_in=0.018, tip=0.017, lift=0.12, force=8.0):
    """Top-down corner pinch at the hull corner nearest the robot (as the pouch r149): pads s_in inside the corner along
    its bisector, pad height max(item middle, support + tip + 2 mm); hold only through the grasp-QC guard. AI-operated."""
    zz_b = body_of(nm); o_ = {}
    mon_start(target=zz_b)
    try:
        open_jaws(side, T=0.3)
        p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
        C_, cc0_, zlo_, ztop_ = flat_corners(zz_b); n_c = len(C_)
        k_best = min(range(n_c), key=lambda k: ahead_of_pelvis(C_[k]) + 0.5 * abs((C_[k] - p_[:2]) @ lat_[:2] - (0.2 if side == "left" else -0.2)))
        X_ = C_[k_best]; e1_ = C_[(k_best + 1) % n_c] - X_; e2_ = C_[(k_best - 1) % n_c] - X_
        w_ = e1_ / np.linalg.norm(e1_) + e2_ / np.linalg.norm(e2_); w_ /= np.linalg.norm(w_)
        G_ = X_ + w_ * s_in
        zp_ = float(max(0.5 * (zlo_ + ztop_), zlo_ + tip + 0.002))
        cd_ = np.r_[-w_[1], w_[0], 0.0]; cd_ = cd_ if cd_ @ lat_ >= 0 else -cd_
        Q_ = {side: q_(R_down(cd_))}
        o_.update(corner=np.round(X_, 3).tolist(), ahead=round(ahead_of_pelvis(G_), 3), z=round(zp_, 3))
        PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(side, G_, ztop_ + 0.06, Q_, speed=0.15), 3).tolist()
        PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(side, G_, zp_, Q_, speed=0.05), 3).tolist()
        if np.linalg.norm(o_["e_down"][:2]) > 0.012 or abs(o_["e_down"][2]) > 0.012:
            raise Abort(f"pads not at the corner: {o_['e_down']}")
        PRE_ACTION("close_jaws", {}); close_jaws(side, force, T=0.8)
        g_ = grip_check(side, None, min_gap=0.003)
        o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}; o_["fingers"] = len(jaw_fingers_on(side, zz_b))
        if g_["ok"] and hold_on(side, zz_b):
            HELD[side] = dict(min_gap=0.003); MON["held"][side] = zz_b; MON["target"] = None; MON["last_touch"][side] = float(d.time)
            z0_ = float(centre(zz_b)[2]); hp_ = ts.ee_pose(side)[0]
            PRE_ACTION("lift", {}); op.move({side: [hp_[0], hp_[1], hp_[2] + lift]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            o_["rose"] = round(float(centre(zz_b)[2]) - z0_, 3)
            cc_ = umb_contacts(zz_b); o_["touching"] = sorted(set(k_[0] for k_ in cc_))
            o_["held"] = bool(HOLD.holding(side) and not hold_lost(side))
    except Abort as ex_:
        o_["abort"] = str(ex_)[:300]
    MON["on"] = False
    o_["Q"] = Q_ if "Q_" in dir() else None
    return o_


def bin_drop(nm, side):
    """Carry the held thing to the rubbish bin by put_away; if it stops with the thing over the opening, let go there."""
    zz_b = body_of(nm); bn_ = body_of("rubbish_bin"); o_ = {}
    mon_start(target=None); MON["held"][side] = zz_b; MON["last_touch"][side] = float(d.time)
    try:
        crouch_holding((side,), H_WALK, 0.0, T=2.0)
        pts_ = put_away(zz_b, side)
        o_["puts"] = str([{k_: v_ for k_, v_ in p_.items() if k_ != "walk"} for p_ in pts_ if isinstance(p_, dict)])[:400]
    except Abort as ex_:
        o_["abort"] = str(ex_)[:300]
    MON["on"] = False
    if HOLD.holding(side):
        lo_, hi_ = obj_box(bn_); plo_, phi_ = obj_box(zz_b)
        over_ = bool(lo_[0] + 0.03 < plo_[0] and phi_[0] < hi_[0] - 0.03 and lo_[1] + 0.03 < plo_[1] and phi_[1] < hi_[1] - 0.03 and plo_[2] > hi_[2] + 0.01)
        o_["over_opening"] = over_
        if over_:
            open_jaws(side, T=0.5); HELD.pop(side, None); MON["held"] = {}; op.run(1.0)
    o_["in"] = bool(inside(zz_b, bn_))
    # off the bin: cancel any lowering, stay tall, step back (the pouch's back-off fell when the pelvis lowered at the bin)
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.4)); op.run(1.0)
    hp_ = ts.ee_pose(side)[0]; op.move({side: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.1, timeout=2.0, tol=0.02)
    rest_hands(SIDES, T=0.6)
    for k_ in range(2):
        if contact_report()["body"] > 1.0 or k_ == 0:
            tmove(fwd=-0.10, carry=("left",), tag="off_bin_tall")
    o_.update(state=state(), fell=fallen())
    return o_
