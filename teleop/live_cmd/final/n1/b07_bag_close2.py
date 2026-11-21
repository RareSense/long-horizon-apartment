ZP2 = 0.031
o_ = {}
mon_start(target=zz_b)
try:
    PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.4)
    G2_ = corner_pinch_plan(zz_b, 3, SD)[0]["G"]
    PRE_ACTION("servo_pads", {}); o_["e"] = np.round(servo_pads(SD, G2_, ZP2, Q_, speed=0.05), 4).tolist()
    print("pad", np.round(pad_mid(SD), 4).tolist(), "jaw tips z", [round(float(d.xpos[m.body(f"{SD}_Dex1_finger_link_{i}").id][2]), 4) for i in (1, 2)], flush=True)
    z0b_ = float(centre(zz_b)[2])
    PRE_ACTION("close_jaws", {}); close_jaws(SD, 8.0, T=1.0)
    g_ = grip_check(SD, None, min_gap=0.004)
    o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
    o_["fingers_on"] = len(jaw_fingers_on(SD, zz_b)); o_["finger_touch"] = finger_touch(SD)
    if g_["ok"] and o_["fingers_on"] >= 2 and hold_on(SD, zz_b):
        hp_ = ts.ee_pose(SD)[0]
        PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.08, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
        o_["rose"] = round(float(centre(zz_b)[2] - z0b_), 3)
        o_["grip2"] = {k: v for k, v in grip_check(SD, None, min_gap=0.004).items() if k in ("ok", "gap", "jaw1_N", "jaw2_N")}
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("OUT", o_, "held", HOLD.holding(SD), "state", state(), "bag", np.round(centre(zz_b), 3).tolist(), flush=True)
print(look3("n1_b07"), flush=True)
