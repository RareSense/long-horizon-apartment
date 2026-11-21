o_ = {}
mon_start(target=zz_b)
try:
    print("pad", np.round(pad_mid(SD), 4).tolist(), "fingers on before", len(jaw_fingers_on(SD, zz_b)), flush=True)
    z0b_ = float(centre(zz_b)[2])
    PRE_ACTION("close_jaws", {}); close_jaws(SD, 8.0, T=0.8)
    g_ = grip_check(SD, None, min_gap=0.004)
    o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    o_["fingers_on"] = len(jaw_fingers_on(SD, zz_b))
    o_["look_closed"] = look_grasp(zz_b, SD, "n1_corner_closed")
    if g_["ok"] and hold_on(SD, zz_b):
        hp_ = ts.ee_pose(SD)[0]
        PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
        o_["rose"] = round(float(centre(zz_b)[2] - z0b_), 3)
        o_["grip2"] = {k: v for k, v in grip_check(SD, None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
        o_["touching"] = sorted(set(k_[0] for k_ in umb_contacts(zz_b))) if "umb_contacts" in globals() else None
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("OUT", o_, "held", HOLD.holding(SD), "state", state(), "bag", np.round(centre(zz_b), 3).tolist(), flush=True)
