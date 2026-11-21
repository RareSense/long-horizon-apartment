import time as _tm


def pinch_cycle(side="left", k=1, s=0.020, stroke_max=0.14, reach=0.42, fwd_extra=0.0):
    """One push cycle from a squat with a corner pinch: let go, hand up, stand, step along the bisector, squat, re-pinch
    (contact-checked), lead-push to the arm's reach."""
    t0_ = _tm.time(); o_ = {}
    C_, c_, z0_, z1_ = flat_corners(UMB)
    w_ = c_ - C_[k]; w_ /= np.linalg.norm(w_)
    pl_ = corner_pinch_plan(UMB, k, side, s)[0]
    open_jaws(side, T=0.3)
    hp_ = pad_mid(side)
    PRE_ACTION("hand_up", {}); servo_pads(side, hp_[:2], 0.12, {side: q_(R_down(pl_["cd"]))}, speed=0.08, n=1)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.0); crouch(0.0, 0.0, T=1.0)
    rest_hands((side,), T=0.5)
    # step so the corner grasp point is 0.20 ahead of the standing pelvis on the plan's stance line
    pl_ = corner_pinch_plan(UMB, k, side, s)[0]
    st_ = np.asarray(pl_["stance"], float)
    p_, yaw_ = base()
    dxy_ = st_[:2] + np.array([np.cos(st_[2]), np.sin(st_[2])]) * fwd_extra - p_[:2]
    R2_ = RM.rz(yaw_)[:2, :2]
    loc_ = R2_.T @ dxy_
    turn_ = float(np.degrees(wrapa(st_[2] - yaw_)))
    o_["step"] = np.round(loc_, 3).tolist(); o_["turn"] = round(turn_, 1)
    tmove(fwd=float(loc_[0]), side=float(loc_[1]), turn=turn_ if abs(turn_) > 3 else 0.0, tag="f12_cycle")
    open_jaws(side, T=0.2)
    PRE_ACTION("squat", {}); crouch(-0.30, 0.6, T=1.0); crouch(-0.40, 0.85, T=1.0)
    Q_, e_, cc_ = repinch(side, k, s)
    o_["repinch"] = (e_, sorted(set(c_[0] for c_ in cc_)), [c_[2] for c_ in cc_][:2])
    top_ = any(abs(c_[2][2]) > 0.5 for c_ in cc_)
    if top_ or len(set(c_[0] for c_ in cc_)) < 2:
        o_["bad_pinch"] = True; return o_
    C_, c_, z0_, z1_ = flat_corners(UMB); W_ = pad_mid(side)[:2] - C_[k]; W_ /= np.linalg.norm(W_)
    o_["ahead0"] = round(ahead_of_pelvis(pad_mid(side)), 3)
    o_["push"] = lead_push(side, W_, Q_, n=8, reach=reach)
    o_["wall_s"] = round(_tm.time() - t0_)
    return o_


SIDE = "left"
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    for i_ in range(2):
        r_ = pinch_cycle(SIDE)
        print("CYCLE", i_, r_, "umb", np.round(centre(UMB)[:2], 3).tolist(), "yaw", round(slab_yaw(), 1), flush=True)
        if r_.get("bad_pinch"):
            break
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
print("state", state(), flush=True)
print(look3("f12_cycle_end"), flush=True)
