# right hand back toward the body (coat; AI-operated)
PRE_ACTION("zz_right_retreat", {})
for zz_t in ((0.28, -0.18, 0.98), (0.18, -0.26, 0.95)):
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.08, step=0.06)
    print("right to", zz_t, zz_r, "at_f R", zz_w().at_fingers("right"), "out", zz_out_parts(), "inside", in_container(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
zz_hand_cloth("left")
a_, b_ = pads("left"); Rn_ = ts.ee_pose("left")[1]
print("left pad rf", np.round(zz_to_rf(pad_mid("left")), 3).tolist(), "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 1], 2).tolist(), "held L", cloth_held("left"), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
