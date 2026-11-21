MON["on"] = False
zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", "0850_act_squat_put")); gait_on(); sync_cloth(force=True)
b_ = body_of("r105i1_shoe"); sd_ = "left"
ax_, c_, zb_ = shoe_axis(b_)
print("at 0850", state(), "touch", finger_touch(sd_, b_), "axis", np.round(ax_, 2).tolist(), "c", np.round(c_, 3).tolist(), "zb", round(zb_, 3), "tilt", round(box_tilt_deg(b_), 1), "pad", np.round(pad_mid(sd_), 3).tolist(), flush=True)
print("ee R", np.round(ts.ee_pose(sd_)[1], 2).tolist(), flush=True)
print(look_hand(sd_, "s04_held_0850"), flush=True)
