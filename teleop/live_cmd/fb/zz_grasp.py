# Stepwise floor cloth grasp at a CHOSEN particle (AI-operated teleop; the steps are those of cloth_skills.grasp_cloth).
def zz_walk_stance(goal, tight=True):
    mon_start(target=None)
    out_ = None
    try:
        phase(f"walk to {zz_BL}")
        fn_ = lambda: walk_to_stance(goal, None)
        out_ = with_tight(fn_) if tight else fn_()
    except Abort as ex_:
        out_ = dict(abort=str(ex_))
    MON["on"] = False
    return out_


def zz_crouch_over(ip, sd):
    """Crouch and bring the open jaws 6 cm above particle ip."""
    PRE_ACTION("zz_crouch_over", dict(ip=int(ip), side=sd))
    pt_ = zz_w().points(0)[ip]
    ok_r, r_ = in_reach(pt_, sd)
    jaw_force[sd] = 20.0; jaw_target[sd] = PRE_OPEN; op.run(0.3)
    crouch(**CROUCH)
    p_, yaw_ = base(); lat_ = RM.rz(yaw_)[:, 1]
    Q_ = {sd: q_(R_down(lat_))}
    lv_ = cloth_level(zz_BL, pt_)
    e1_ = servo_pads(sd, pt_[:2], lv_ + 0.06, Q_, speed=0.2)
    return dict(in_reach=ok_r, rel=r_, above_err=np.round(e1_, 4).tolist(), pelvis=d.qpos[:3].round(3).tolist(), Q=Q_)


def zz_jaws_down(sd, Q_):
    PRE_ACTION("zz_jaws_down", dict(side=sd))
    a_, b_ = pads(sd)
    lvs_ = [v_ for v_ in (cloth_level(zz_BL, x_, r=0.02) for x_ in (a_, b_)) if v_ is not None]
    if not lvs_:
        return dict(error="no cloth under the pads")
    want_ = max(min(lvs_) - PRESS, 0.006)
    for it_ in range(4):
        low_ = pad_low(sd)
        if abs(low_ - want_) < 0.0007:
            break
        hp_ = ts.ee_pose(sd)[0]
        op.move({sd: [hp_[0], hp_[1], hp_[2] + (want_ - low_)]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.003); op.run(0.3)
    return dict(pad_low=round(pad_low(sd), 4), wanted=round(want_, 4))


def zz_close_lock(sd, T=4.0):
    PRE_ACTION("zz_close_lock", dict(side=sd))
    squeeze_on(sd, zz_BL)
    t0_ = d.time
    while d.time - t0_ < T:
        op.run(0.1)
        c_ = SQ[sd]
        if c_["e"] > 0.9 and min(c_["F1"], c_["F2"]) > 3.0 and d.time - t0_ > 0.5:
            break
    op.run(0.4)
    c_ = dict(SQ[sd]); c_.pop("w")
    cg_ = zz_w().caught(sd)
    n_c = lock_grip(sd)
    out_ = dict(gap_cm=round(gap(sd) * 100, 2), F1=round(c_["F1"], 1), F2=round(c_["F2"], 1), caught=int(n_c), held=len(LOCK[sd][1]) if sd in LOCK else 0,
                caught_uv_mean=np.round(zz_uv()[cg_].mean(0), 3).tolist() if len(cg_) else None)
    if not n_c:
        squeeze_off(sd)
    else:
        HELD[sd] = dict(cloth=zz_BL)
    EVENTS.append(dict(t=round(float(d.time), 2), ev="zz_close_lock", side=sd, **out_))
    return out_


def zz_release(sd, T=0.35):
    """Let the cloth go: the hold ends, the jaws open in three steps."""
    PRE_ACTION("zz_release", dict(side=sd))
    unlock_grip(sd); squeeze_off(sd)
    for jv_ in (0.012, 0.022, JAW_OPEN):
        jaw_force[sd] = 20.0; jaw_target[sd] = jv_; op.run(T)
    HELD.pop(sd, None)
    return zz_w().at_fingers(sd)


print("[zz] grasp steps loaded", flush=True)
