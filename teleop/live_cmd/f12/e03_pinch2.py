SIDE = "left"; K_SE = 1; S_IN = 0.020
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
o_ = {}
try:
    pl2_ = corner_pinch_plan(UMB, K_SE, SIDE, S_IN)[0]
    G_ = pl2_["G"]; CDp = pl2_["cd"]; QP = {SIDE: q_(R_down(CDp))}
    hp_ = pad_mid(SIDE)
    PRE_ACTION("hand_up", {}); servo_pads(SIDE, hp_[:2], 0.07, QP, speed=0.05, n=2)
    o_["e_above"] = np.round(servo_pads(SIDE, G_, 0.07, QP, speed=0.05, n=3), 4).tolist()
    PRE_ACTION("hand_down", {}); o_["e_down"] = np.round(servo_pads(SIDE, G_, 0.016, QP, speed=0.04, n=3), 4).tolist()
    o_["pad"] = np.round(pad_mid(SIDE), 3).tolist(); o_["G"] = np.round(G_, 3).tolist()
    o_["c_open"] = [c_ for c_ in umb_contacts() if c_[0] != "world"]
    PRE_ACTION("pinch_close", {}); close_jaws(SIDE, 14.0, T=0.8)
    o_["c_closed"] = [c_ for c_ in umb_contacts() if c_[0] != "world"]
    g_ = grip_check(SIDE, None, min_gap=0.004)
    o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), umb=np.round(centre(UMB)[:2], 3).tolist())
print("PINCH2", o_, flush=True)
pm_ = pad_mid(SIDE)
print(close(os.path.join(TELE_DIR, "f12_e03_pinch.jpg"), np.r_[pm_[:2] + np.array([0.30, -0.30]), 0.20], np.r_[pm_[:2], 0.01], "pinch2"), flush=True)
