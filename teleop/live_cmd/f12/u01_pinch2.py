exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\u00_helpers.py", encoding="utf-8").read())
P_, c_ = corner_points()
print("corners", [np.round(p_["X"], 3).tolist() for p_ in P_], "centre", np.round(c_, 3).tolist(), flush=True)
ST, WHO, SPAN = edge_stance(1, 2)
print("stance", np.round(ST, 3).tolist(), "deg", round(np.degrees(ST[2]), 1), "who", WHO, "span", round(SPAN, 3), flush=True)
o_ = {}
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    w_ = walk_tight(ST)
    o_["walk"] = {k_: v_ for k_, v_ in (w_ or {}).items() if k_ in ("ok", "err_xy", "err_yaw")} if isinstance(w_, dict) else str(w_)[:200]
    for s_ in SIDES:
        open_jaws(s_, T=0.2)
    PRE_ACTION("squat", {}); crouch(-0.30, 0.6, T=1.0); crouch(-0.40, 0.85, T=1.0)
    P_, c_ = corner_points()
    Q2 = {s_: q_(R_down(P_[WHO[s_]]["cd"])) for s_ in SIDES}
    for s_ in SIDES:
        G_ = P_[WHO[s_]]["G"]
        o_[s_ + "_ahead_lat"] = (round(ahead_of_pelvis(G_), 3),)
        PRE_ACTION("hand_above", dict(side=s_)); o_[s_ + "_e_above"] = np.round(servo_pads(s_, G_, 0.07, {s_: Q2[s_]}, speed=0.06, n=3), 3).tolist()
    for s_ in SIDES:
        G_ = P_[WHO[s_]]["G"]
        PRE_ACTION("hand_down", dict(side=s_)); o_[s_ + "_e_down"] = np.round(servo_pads(s_, G_, 0.016, {s_: Q2[s_]}, speed=0.04, n=3), 3).tolist()
    o_["open_contacts"] = [c_ for c_ in umb_contacts() if c_[0] not in ("world",)]
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), umb=np.round(centre(UMB)[:2], 3).tolist())
print("U01", o_, flush=True)
for s_ in SIDES:
    pm_ = pad_mid(s_)
    print(close(os.path.join(TELE_DIR, f"f12_u01_{s_}.jpg"), np.r_[pm_[:2] + np.array([0.25, 0.0]) + (np.array([0, 0.25]) if s_ == "right" else np.array([0, -0.25])), 0.22], np.r_[pm_[:2], 0.01], f"u01 {s_}"), flush=True)
