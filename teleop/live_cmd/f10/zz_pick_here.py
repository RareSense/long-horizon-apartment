def zz_pick_here(b_, side, force=12.0):
    """pick_floor's crouch-grasp-lift from where the robot stands (no stance search): the grasp point must be in reach."""
    out_ = dict(reach=None)
    gp_ = grasp_plan(b_)
    out_["reach"] = in_reach(gp_["point"], side)
    open_jaws(side, T=0.2)
    p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
    gp_ = grasp_plan(b_, near=lat_) or gp_
    cd_ = max(gp_["closes"], key=lambda c: abs(c @ lat_)) if gp_["closes"] else lat_
    if cd_ @ lat_ < 0: cd_ = -cd_
    Q_ = {side: q_(R_down(cd_))}
    gc_ = dict(min_gap=0.0015 if gp_["wall"] else 0.004, at=gp_["at"])
    PRE_ACTION("crouch", {}); crouch(T=PICK["t_crouch"], **CROUCH)
    e1_ = servo_pads(side, gp_["point"][:2], gp_["top"] + 0.06, Q_, speed=PICK["v_above"])
    gp_ = grasp_plan(b_, near=cd_) or gp_
    e2_ = servo_pads(side, gp_["point"][:2], gp_["z"], Q_, speed=PICK["v_down"])
    out_.update(e_above=np.round(e1_, 3).tolist(), e_down=np.round(e2_, 3).tolist(), width=gp_.get("width"))
    z0_ = centre(b_)[2]
    PRE_ACTION("close_jaws", {}); close_jaws(side, force, T=PICK["t_close"])
    g1_ = grip_check(side, b_, **gc_)
    out_["grip"] = {k: g1_.get(k) for k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    if g1_["ok"]:
        hold_on(side, b_)
        hp_ = ts.ee_pose(side)[0]
        op.move({side: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
        out_["rose"] = round(float(centre(b_)[2] - z0_), 3)
        HELD[side] = gc_
    out_["look"] = look_grasp(b_, side, "pick_here")
    return out_
