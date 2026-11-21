# left hold: fingers turned nearly straight down (nothing can lie on them), jaws side by side, a little back toward the body (AI-operated)
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
a_ = np.radians(ZZ_TILT)
zz_QLV = {"left": q_(zz_R(np.sin(a_) * zz_fwd + np.cos(a_) * np.array([0, 0, -1.0]), zz_lat))}
PRE_ACTION("zz_left_vertical", {})
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=zz_QLV, speed=0.05, step=0.04)
    Rn_ = ts.ee_pose("left")[1]; pa_, pb_ = pads("left"); Rb_ = RM.rz(base()[1])
    print("left to", zz_t, zz_r, "fingers rf", np.round(Rb_.T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(Rb_.T @ Rn_[:, 1], 2).tolist(), "pads z", round(float(pa_[2]), 3), round(float(pb_[2]), 3), "held L", cloth_held("left"),
          "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "knees", zz_knees(), "fell", fallen(), flush=True)
zz_hand_cloth("left")
hc_ = obj_rect(zz_hb()).c
print("left pad r from centre", round(float(np.linalg.norm(pad_mid("left")[:2] - hc_)), 3), "tilt", round(pelvis_tilt(), 3), flush=True)
print("look hand", look_hand("left", "g39_left"), flush=True)
