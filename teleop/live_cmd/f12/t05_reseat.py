def reseat(side, d_mm=None, soft=6.0, pitch_to=None, tag="t05"):
    """Re-seat the bar in one jaw pair: the squeeze eased to `soft` N, the hand slid along its own fingers so the bar comes
    to the pads' middle (and optionally re-pitched), the squeeze back to SH['squeeze']. The other hand holds still."""
    mon_start(target=None); MON["held"] = {s_: SB for s_ in SIDES}; MON["start"].pop(SB, None); MON["t_max"] = 6000.0
    o_ = {}
    try:
        st_ = sh_seat(SB)[side]
        d_ = (st_["seat_mm"] if d_mm is None else d_mm) / 1000.0
        fx_ = ts.ee_pose(side)[1][:, 0]
        other_ = "right" if side == "left" else "left"
        hold_other_ = dict(cmd="ee", name=other_, mode="velocity", linear=[0, 0, 0], frame="world", ttl=0.3)
        PRE_ACTION("sc_reseat_soft", dict(side=side, soft=soft))
        jaw_force[side] = float(soft); op.run(0.4, [hold_other_])
        pit_ = {other_: sh_seat(SB)[other_]["pitch"], side: st_["pitch"] if pitch_to is None else float(pitch_to)}
        tg_ = {other_: pad_mid(other_).copy(), side: pad_mid(side) + fx_ * d_}
        PRE_ACTION("sc_reseat_slide", dict(side=side, d=round(d_, 4)))
        o_["err"] = both_move(tg_, sh_level_Q(pit_), speed=0.01, tol=0.003)
        op.run(0.3)
        jaw_force[side] = float(SH["squeeze"]); op.run(0.6, [hold_other_])
    except Abort as ex_:
        o_["abort"] = str(ex_)[:300]
    MON["on"] = False
    print("RESEAT", o_, flush=True)
    return sc_report(tag)


print("jaw_force now", {s_: jaw_force[s_] for s_ in SIDES}, "target", {s_: round(float(jaw_target[s_]), 4) for s_ in SIDES}, flush=True)
R2 = reseat("right", tag="t05a")
