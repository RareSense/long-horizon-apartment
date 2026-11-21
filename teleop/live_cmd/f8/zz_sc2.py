# Scooter r126 with RE-GRIP cycles (AI-operated): every turn step = lift -> small turn -> set down -> jaws open -> hands
# back onto the grip points -> close -> lift. Why: the bar twists in the jaws during turns (2.2 -> 3.5 -> 13 cm off in three
# 6 deg steps, this session, ckpts 0567-0587); a fresh grip after each step resets that error.
R_fwd = globals().get("_R_FWD0") or R_fwd

def zz_regrip(b_, tag):
    out_ = {}
    PRE_ACTION("sc_set_down", dict(tag=tag))
    out_["down"] = sc_set_down(b_, speed=0.03, max_dz=0.05)
    for s_ in SIDES:
        open_jaws(s_, T=0.05); ts.ctrl.ext.pop(f"hold_{s_}", None)
    op.run(0.4)
    MON["held"] = {}; MON["ignore_names"] = tuple(set(MON.get("ignore_names", ())) | {b_})
    _, fwd_, _ = sc_grip_points(b_)
    Q_ = {s_: q_(R_fwd(fwd_)) for s_ in SIDES}
    both_move({s_: pad_mid(s_) - np.r_[fwd_ * 0.08, 0.0] for s_ in SIDES}, Q_, speed=0.12, tol=0.01)
    PRE_ACTION("sc_hands_to", dict(tag=tag))
    sc_hands_to(b_, "pre"); e2_ = sc_hands_to(b_, "on", speed=0.1)
    g_ = sc_close(b_, force=14.0)
    G_, _, _ = sc_grip_points(b_)
    ok_ = all(g_[s_].get("gap", 0) > 0.0015 and g_[s_].get("jaw1_N", 0) > 1.5 and g_[s_].get("jaw2_N", 0) > 1.5 and float(np.linalg.norm(pad_mid(s_) - G_[s_])) < 0.03 for s_ in SIDES)
    out_["grip_ok"] = ok_
    out_["pad_err"] = {s_: round(float(np.linalg.norm(pad_mid(s_) - G_[s_])), 3) for s_ in SIDES}
    if not ok_:
        raise Abort(f"re-grip failed at {tag}: {str(g_)[:200]}")
    for s_ in SIDES:
        jaw_target[s_] = 0.0; jaw_force[s_] = 20.0
        ts.ctrl.ext[f"hold_{s_}"] = (f"{s_}_wrist_yaw_link", np.array([0.165, 0.0, 0.0]), np.array([0.0, 0.0, -9.81 * SC_PARK["hand_kg"]]))
    op.run(0.3)
    MON["held"] = {s_: b_ for s_ in SIDES}
    for s_ in SIDES:
        MON["last_touch"][s_] = float(d.time)
    MON["start"][b_] = d.xpos[m.body(b_).id].copy() if b_ in MON.get("start", {}) else None
    MON["start"].pop(b_, None)
    PRE_ACTION("sc_lift", dict(tag=tag))
    out_["lift"] = {k_: v_ for k_, v_ in sc_lift(b_, dz=0.03).items() if k_ in ("lowest", "tilt_deg")}
    ok2_, t_, e_ = _sc_in_jaws(b_)
    if not ok2_:
        raise Abort(f"bar out after the re-grip lift at {tag}: {t_} {e_}")
    SC_REL.clear(); _sc_rel_save()
    return out_

def zz_turn_step(b_, deg, tag):
    r_ = tmove(carry=tuple(SIDES), turn=float(deg), tag=tag)
    if MON.get("why"):
        raise Abort(MON["why"])
    ok_, t_, e_ = _sc_in_jaws(b_)
    sp_ = scooter_parts(b_)
    rec_ = dict(tag=tag, at=r_["at"], yaw=r_["yaw_deg"], deck_deg=round(float(np.degrees(np.arctan2(sp_["deck"][1], sp_["deck"][0]))), 1), pad_to_bar=e_, in_jaws=ok_)
    if not ok_:
        raise Abort(f"bar out of the jaws after {tag}: {rec_}")
    return rec_

def zz_fwd_step(b_, dist, tag):
    r_ = tmove(carry=tuple(SIDES), fwd=float(dist), tag=tag)
    if MON.get("why"):
        raise Abort(MON["why"])
    ok_, t_, e_ = _sc_in_jaws(b_)
    sp_ = scooter_parts(b_)
    rec_ = dict(tag=tag, at=r_["at"], yaw=r_["yaw_deg"], deck_deg=round(float(np.degrees(np.arctan2(sp_["deck"][1], sp_["deck"][0]))), 1), pad_to_bar=e_, in_jaws=ok_)
    if not ok_:
        raise Abort(f"bar out of the jaws after {tag}: {rec_}")
    return rec_

def zz_pivot_step(b_, deg, tag, Lw=0.48):
    """Turn deg (left +) about the scooter's far wheel: the pelvis moves on the circle round it (side step + turn)."""
    sp_ = scooter_parts(b_)
    W_ = sp_["stem"][:2] + sp_["deck"] * Lw
    p_, y_ = base(); p_ = p_[:2]
    th_ = np.radians(deg); c_, s_ = np.cos(th_), np.sin(th_)
    pn_ = W_ + np.array([[c_, -s_], [s_, c_]]) @ (p_ - W_)
    yg_ = y_ + th_
    loc_ = RM.rz(yg_)[:2, :2].T @ (pn_ - p_)
    r_ = tmove(carry=tuple(SIDES), turn=float(deg), fwd=float(loc_[0]), side=float(loc_[1]), tag=tag)
    if MON.get("why"):
        raise Abort(MON["why"])
    ok_, t_, e_ = _sc_in_jaws(b_)
    sp2_ = scooter_parts(b_)
    rec_ = dict(tag=tag, asked=np.round(loc_, 3).tolist(), at=r_["at"], yaw=r_["yaw_deg"], deck_deg=round(float(np.degrees(np.arctan2(sp2_["deck"][1], sp2_["deck"][0]))), 1), pad_to_bar=e_, in_jaws=ok_, W=np.round(W_, 3).tolist())
    if not ok_:
        raise Abort(f"bar out of the jaws after {tag}: {rec_}")
    return rec_

def zz_sc_take2(b_):
    """walk to the take stance, full height, both hands onto the bar ends (fingers forward), close, load told, lift 3 cm."""
    SP_ = scooter_parts(b_)
    b2 = SP_["bar_c"][:2] - SP_["deck"] * SC_PARK["bar_d"]
    st_ = (float(b2[0]), float(b2[1]), float(np.arctan2(SP_["deck"][1], SP_["deck"][0])))
    try:
        walk_to_stance(st_, name=b_)
    except RuntimeError as ex_:
        if "no free path" not in str(ex_) and "no place" not in str(ex_): raise
        with_tight(lambda: walk_to_stance(st_, name=b_))
    if MON.get("why"): raise Abort(MON["why"])
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.8)
    PRE_ACTION("sc_hands_to", {}); sc_hands_to(b_, "pre"); sc_hands_to(b_, "on")
    PRE_ACTION("sc_close", {}); g_ = sc_close(b_)
    G_, _, _ = sc_grip_points(b_)
    ok_ = all(g_[s_].get("gap", 0) > 0.0015 and g_[s_].get("jaw1_N", 0) > 1.5 and g_[s_].get("jaw2_N", 0) > 1.5 and float(np.linalg.norm(pad_mid(s_) - G_[s_])) < 0.03 for s_ in SIDES)
    if not ok_: raise Abort(f"take grip failed {str(g_)[:200]}")
    for s_ in SIDES:
        jaw_target[s_] = 0.0; jaw_force[s_] = 20.0
        ts.ctrl.ext[f"hold_{s_}"] = (f"{s_}_wrist_yaw_link", np.array([0.165, 0.0, 0.0]), np.array([0.0, 0.0, -9.81 * SC_PARK["hand_kg"]]))
    op.run(0.3); MON["held"] = {s_: b_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(b_, None)
    for s_ in SIDES: MON["last_touch"][s_] = float(d.time)
    PRE_ACTION("sc_lift", {}); l_ = sc_lift(b_, dz=0.03)
    ok2_, t_, e_ = _sc_in_jaws(b_)
    if not ok2_: raise Abort(f"bar out after lift {t_} {e_}")
    SC_REL.clear(); _sc_rel_save()
    return dict(stance=np.round(st_, 3).tolist(), lift=l_.get("lowest"), pad_to_bar=e_)

def zz_sc_state(b_):
    sp_ = scooter_parts(b_); W_ = sp_["stem"][:2] + sp_["deck"] * 0.48
    p_, y_ = base()
    return dict(pel=np.round(p_[:2], 3).tolist(), yaw=round(float(np.degrees(y_)), 1), deck=round(float(np.degrees(np.arctan2(sp_["deck"][1], sp_["deck"][0]))), 1), W=np.round(W_, 3).tolist(), bar=np.round(sp_["bar_c"][:2], 3).tolist(), pads=_sc_in_jaws(b_)[2])
