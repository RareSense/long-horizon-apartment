p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
a_ = np.radians(ZZ_TILT)
zz_QRT = {"right": q_(zz_R(np.sin(a_) * zz_fwd + np.cos(a_) * np.array([0, 0, -1.0]), zz_lat))}
PRE_ACTION("zz_tilt_fingers", dict(tilt=ZZ_TILT))
# first up a little, turn, then to the fold
r0_ = zz_pads_to("right", pad_mid("right") + np.array([0, 0.0, 0.05]), Q=zz_QRT, speed=0.04, step=0.03)
tg_ = zz_w().points(0)[ZZ_IT2].copy()
r1_ = zz_pads_to("right", np.r_[tg_[:2], tg_[2] + 0.05], Q=zz_QRT, speed=0.04, step=0.03)
Rn_ = ts.ee_pose("right")[1]
print("tilted: ", r1_, "fingers", np.round(Rn_[:, 0], 2).tolist(), "close", np.round(Rn_[:, 1], 2).tolist(), "tgt", np.round(tg_, 3).tolist(), "in_pads", zz_in_pads("right", ZZ_IT2), "pad_low", round(pad_low("right"), 3), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", [v_[0] for k_, v_ in zz_knees().items() if "knee" in k_], flush=True)
