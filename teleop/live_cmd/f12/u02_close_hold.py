o_ = {}
P_, c_ = corner_points()
Q2 = {s_: q_(R_down(P_[WHO[s_]]["cd"])) for s_ in SIDES}
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    PRE_ACTION("pinch_close_both", {})
    for s_ in SIDES:
        jaw_force[s_] = 14.0; jaw_target[s_] = 0.0
    op.run(0.9)
    cc_ = umb_contacts()
    o_["contacts"] = [c_ for c_ in cc_ if c_[0] != "world"]
    chk_ = {s_: pinch_ok(s_, cc_) for s_ in SIDES}
    o_["check"] = chk_
    o_["grip"] = {s_: {k: v for k, v in grip_check(s_, None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")} for s_ in SIDES}
    others_ = [c_ for c_ in cc_ if c_[0] not in ("world",) and ":" not in c_[0]]
    o_["others"] = others_
    if all(chk_[s_][0] for s_ in SIDES) and not others_:
        hold_on("left", UMB, 0.5); hold_on("right", UMB, 0.5)
        z0_ = float(centre(UMB)[2])
        PRE_ACTION("lift_both", {})
        e_ = both_move({s_: pad_mid(s_) + np.array([0, 0, 0.04]) for s_ in SIDES}, Q2, speed=0.05)
        op.run(0.5)
        o_["lift_err"] = e_; o_["rose"] = round(float(centre(UMB)[2]) - z0_, 3)
        o_["floor_contacts_after"] = [c_ for c_ in umb_contacts() if c_[0] == "world"]
        o_["hold_err"] = {s_: round(HOLD.items[s_]["err"], 4) for s_ in SIDES if s_ in HOLD.items}
        o_["lost"] = {s_: hold_lost(s_) for s_ in SIDES}
    else:
        o_["no_hold"] = "pinch check failed"
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), umb=np.round(centre(UMB), 3).tolist())
print("U02", o_, flush=True)
print(look3("f12_u02_lift"), flush=True)
