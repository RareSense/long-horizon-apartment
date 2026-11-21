MON["on"] = False
b_ = body_of("r105i2_shoe"); sd_ = "left"
for ck_ in ("1147_act_squat_put", "1148_act_hand_over_spot2", "1155_act_hand_over_spot2", "1159_act_hand_down"):
    zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", ck_)); gait_on()
    ax_, c_, zb_ = shoe_axis(b_); pm_ = pad_mid(sd_); p_, y_ = base()
    print(ck_, "pelvis", np.round(p_, 3).tolist(), "pad", np.round(pm_, 3).tolist(), "rel", np.round(RM.rz(y_)[:2, :2].T @ (pm_[:2] - p_[:2]), 3).tolist(), "shoe c", np.round(c_, 3).tolist(), "zb", round(zb_, 3), "tilt", round(box_tilt_deg(b_), 1), "axis", np.round(ax_, 2).tolist(), "touch", finger_touch(sd_, b_), flush=True)
sync_cloth(force=True)
print(look_hand(sd_, "s11_at_1159"), flush=True)
