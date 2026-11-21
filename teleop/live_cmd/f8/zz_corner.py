def zz_corner_plan(k_, side, s_=0.03):
    C_, c_, z0_, z1_ = zz_bag_corners()
    X_ = C_[k_]; n_ = len(C_)
    e1_ = C_[(k_ + 1) % n_] - X_; e2_ = C_[(k_ - 1) % n_] - X_
    w_ = e1_ / np.linalg.norm(e1_) + e2_ / np.linalg.norm(e2_); w_ /= np.linalg.norm(w_)
    G_ = X_ + w_ * s_
    sg_ = 1.0 if side == "left" else -1.0
    out_ = []
    for fw_ in (w_, -w_):
        yaw_ = float(np.arctan2(fw_[1], fw_[0])); R2_ = RM.rz(yaw_)[:2, :2]
        P_ = G_ - R2_ @ np.array([X_REL, sg_ * Y_REL])
        out_.append(dict(stance=(float(P_[0]), float(P_[1]), yaw_), free=bool(with_tight(lambda: room_grid((zz_b,)).free(P_))), G=G_, cd=np.array([-fw_[1], fw_[0]]), corner=X_, top=z1_))
    return out_


def zz_corner_try(k_, side, s_=0.03, z_=0.0255, force=8.0, pick=None):
    plans_ = zz_corner_plan(k_, side, s_)
    pl_ = pick if pick is not None else next((p_ for p_ in plans_ if p_["free"]), plans_[0])
    o_ = dict(corner=np.round(pl_["corner"], 3).tolist(), G=np.round(pl_["G"], 3).tolist(), stance=np.round(pl_["stance"], 3).tolist(), free=pl_["free"])
    mon_start(target=zz_b)
    try:
        if base()[0][2] < 0.6:
            stand_up()
        rest_hands(SIDES, T=0.6)
        w_ = walk_tight(pl_["stance"])
        o_["walk_err"] = w_.get("err_xy") if isinstance(w_, dict) else str(w_)[:100]
        o_["reach"] = in_reach(pl_["G"], side)
        # re-plan from the bag as it is now (the walk may have nudged it)
        pl2_ = zz_corner_plan(k_, side, s_)[0 if pl_ is plans_[0] else 1]
        G_ = pl2_["G"]; cd_ = pl2_["cd"]
        open_jaws(side, T=0.3)
        crouch(T=1.8, **CROUCH)
        Q_ = {side: q_(R_down(cd_))}
        o_["e_above"] = np.round(servo_pads(side, G_, pl_["top"] + 0.06, Q_, speed=0.2), 4).tolist()
        o_["e_down"] = np.round(servo_pads(side, G_, z_, Q_, speed=0.06), 4).tolist()
        o_["look_open"] = look_grasp(zz_b, side, "corner_open")
        z0_ = centre(zz_b)[2]
        close_jaws(side, force, T=0.8)
        g_ = grip_check(side, None, min_gap=0.004)
        o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
        o_["touch"] = finger_touch(side)
        o_["look_closed"] = look_grasp(zz_b, side, "corner_closed")
        if g_["ok"]:
            hold_on(side, zz_b)
            hp_ = ts.ee_pose(side)[0]
            op.move({side: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
            o_["rose"] = round(float(centre(zz_b)[2] - z0_), 3)
            o_["grip2"] = {k: v for k, v in grip_check(side, None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
            o_["look_lift"] = look_grasp(zz_b, side, "corner_lift")
    except Abort as ex_:
        o_["abort"] = str(ex_)
    MON["on"] = False
    o_.update(state=state(), fell=fallen(), bag=np.round(centre(zz_b), 3).tolist())
    return o_
