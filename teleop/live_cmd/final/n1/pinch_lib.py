# corner pinch from a stance already reached (night fix 21 Nov, AI-operated): park the other hand ahead (it hit the toy
# basket in the squat), squat, pads above then down at z_, close, hold only through the guard (both fingers on it).
def n1_corner_pinch(b_, k_, SD, z_=0.0255, s_=0.03, force=8.0, park=True):
    OT = "right" if SD == "left" else "left"
    pl_ = corner_pinch_plan(b_, k_, SD, s_)[0]
    o_ = dict(G=np.round(pl_["G"], 3).tolist(), z=z_)
    mon_start(target=b_)
    try:
        p_, yaw_ = base(); fw_ = RM.rz(yaw_)[:, 0]; lat_ = RM.rz(yaw_)[:, 1]
        if park:
            T_ = p_ + 0.30 * fw_ + (0.12 if OT == "left" else -0.12) * lat_; T_[2] = 0.42
            PRE_ACTION("park_other_hand", dict(side=OT)); op.move({OT: T_.tolist()}, speed=0.15, timeout=3.0, tol=0.02); op.run(0.3)
        open_jaws(SD, T=0.3)
        PRE_ACTION("crouch", dict(CROUCH)); crouch(T=1.8, **CROUCH)
        pl_ = corner_pinch_plan(b_, k_, SD, s_)[0]; G_ = pl_["G"]
        Q_ = {SD: q_(R_down(pl_["cd"]))}
        PRE_ACTION("servo_pads", {}); o_["e_above"] = np.round(servo_pads(SD, G_, pl_["top"] + 0.06, Q_, speed=0.2), 4).tolist()
        PRE_ACTION("servo_pads", {}); o_["e_down"] = np.round(servo_pads(SD, G_, z_, Q_, speed=0.06), 4).tolist()
        z0b_ = float(centre(b_)[2]); c0_ = centre(b_).copy()
        PRE_ACTION("close_jaws", {}); close_jaws(SD, force, T=0.8)
        g_ = grip_check(SD, None, min_gap=0.004)
        o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
        o_["fingers_on"] = len(jaw_fingers_on(SD, b_)); o_["moved"] = round(float(np.linalg.norm(centre(b_)[:2] - c0_[:2])), 3)
        if g_["ok"] and hold_on(SD, b_):
            HELD[SD] = dict(min_gap=0.004); MON["held"][SD] = b_; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
            o_["rose"] = round(float(centre(b_)[2] - z0b_), 3)
            o_["grip2"] = {k: v for k, v in grip_check(SD, None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
        o_["Q"] = Q_
    except Abort as ex_:
        o_["abort"] = str(ex_)
    MON["on"] = False
    o_.update(held=bool(HOLD.holding(SD)), state=state(), at=np.round(centre(b_), 3).tolist())
    return o_
