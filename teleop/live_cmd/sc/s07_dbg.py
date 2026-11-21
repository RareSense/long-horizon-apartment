MON["on"] = False
zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", "0911_act_hand_over_spot")); gait_on(); sync_cloth(force=True)
b_ = body_of("r105i1_shoe"); sd_ = "left"
ax_, c_, zb_ = shoe_axis(b_); pm_ = pad_mid(sd_); p_, y_ = base()
print("0911", state(), "pad", np.round(pm_, 3).tolist(), "rel", np.round(RM.rz(y_)[:2, :2].T @ (pm_[:2] - p_[:2]), 3).tolist(), "shoe c", np.round(c_, 3).tolist(), "zb", round(zb_, 3), flush=True)
print("ee R", np.round(ts.ee_pose(sd_)[1], 2).tolist(), "ee mode", {k_: str(v_)[:80] for k_, v_ in (ts.ee.get(sd_) or {}).items()} if isinstance(getattr(ts, "ee", None), dict) else None, flush=True)
Q_ = {sd_: q_(ts.ee_pose(sd_)[1])}
for k_ in range(3):
    e_ = servo_pads(sd_, pad_mid(sd_)[:2] + np.array([0.04, 0.0]), pad_mid(sd_)[2], Q_, speed=0.05, n=2)
    pm_ = pad_mid(sd_)
    print("step", k_, "err", np.round(e_, 3).tolist(), "pad", np.round(pm_, 3).tolist(), "rel", np.round(RM.rz(y_)[:2, :2].T @ (pm_[:2] - p_[:2]), 3).tolist(), "touch", finger_touch(sd_, b_), "contacts", contact_report(), flush=True)
