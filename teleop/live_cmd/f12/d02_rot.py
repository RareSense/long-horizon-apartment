SIDE = "left"; U = np.array([-1.0, 0.0])
Q2 = {SIDE: q_(R_down(U))}
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    pm_ = pad_mid(SIDE)
    PRE_ACTION("hand_rot", {}); servo_pads(SIDE, pm_[:2] - U * 0.02, 0.06, Q2, speed=0.05, n=2)
    print("e", np.round(servo_pads(SIDE, pm_[:2] - U * 0.02, 0.022, Q2, speed=0.04, n=3), 3).tolist(), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
pm_ = pad_mid(SIDE)
print("pad", np.round(pm_, 3).tolist(), "state", state(), flush=True)
print(close(os.path.join(TELE_DIR, "f12_d02_side.jpg"), np.r_[pm_[:2] + np.array([0.0, -0.45]), 0.12], np.r_[pm_[:2], 0.02], "pad side rot"), flush=True)
print(close(os.path.join(TELE_DIR, "f12_d02_front.jpg"), np.r_[pm_[:2] + np.array([-0.45, -0.05]), 0.12], np.r_[pm_[:2], 0.02], "pad front rot"), flush=True)
