o_ = {}
P_, c_ = corner_points()
Q2 = {s_: q_(R_down(P_[WHO[s_]]["cd"])) for s_ in SIDES}
CARRY_Z = 0.62
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    sq_ = RM.rz(ST[2])[:2, :2]
    tg_ = {}
    for s_ in SIDES:
        rel_ = sq_.T @ (pad_mid(s_)[:2] - np.asarray(ST[:2]))
        tg_[s_] = np.r_[np.asarray(ST[:2]) + sq_ @ rel_, CARRY_Z]
        o_[s_ + "_rel"] = np.round(rel_, 3).tolist()
    also_ = [dict(cmd="ee", name=s_, mode="pose", position=[float(v_) for v_ in (ts.ee_pose(s_)[0] + (tg_[s_] - pad_mid(s_)))], quaternion=Q2[s_], frame="world", speed=0.25, accel=2.0, guard=False) for s_ in SIDES]
    PRE_ACTION("stand_with_umbrella", {})
    crouch_holding((), -0.20, 0.35, T=1.6, also=also_)
    crouch_holding((), 0.0, 0.0, T=1.6, also=also_)
    o_["e_carry"] = both_move(tg_, Q2, speed=0.15)
    op.run(0.5)
    o_["hold_err"] = {s_: round(HOLD.items[s_]["err"], 4) for s_ in SIDES if s_ in HOLD.items}
    o_["lost"] = {s_: hold_lost(s_) for s_ in SIDES}
    o_["umb_contacts"] = [c_ for c_ in umb_contacts() if ":" not in c_[0]]
    o_["umb_tilt_deg"] = round(box_tilt_deg(UMB), 1)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), umb=np.round(centre(UMB), 3).tolist(), fell=fallen())
print("U03", o_, flush=True)
print(look3("f12_u03_stand"), flush=True)
