# right hand back toward the body; left hold a little lower with the jaws side by side (fingers down-forward) for the release (AI-operated)
PRE_ACTION("zz_right_retreat", {})
for zz_t in ((0.28, -0.18, 0.98), (0.18, -0.26, 0.95)):
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.08, step=0.06)
    print("right to", zz_t, zz_r, "at_f R", zz_w().at_fingers("right"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
a_ = np.radians(35.0)
zz_QLT = {"left": q_(zz_R(np.sin(a_) * zz_fwd + np.cos(a_) * np.array([0, 0, -1.0]), zz_lat))}
PRE_ACTION("zz_left_lower", {})
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=zz_QLT, speed=0.05, step=0.04)
    Rn_ = ts.ee_pose("left")[1]; pa_, pb_ = pads("left"); Rb_ = RM.rz(base()[1])
    print("left to", zz_t, zz_r, "fingers rf", np.round(Rb_.T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(Rb_.T @ Rn_[:, 1], 2).tolist(), "pads z", round(float(pa_[2]), 3), round(float(pb_[2]), 3), "held L", cloth_held("left"),
          "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "knees", zz_knees(), "fell", fallen(), flush=True)
hc_ = obj_rect(zz_hb()).c
print("left pad r from centre", round(float(np.linalg.norm(pad_mid("left")[:2] - hc_)), 3), "tilt", round(pelvis_tilt(), 3), "pelvis", state()["pelvis"], flush=True)
print("look", zz_look(np.array([hc_[0], hc_[1], 0.7]), "g36_prep_left", dist=1.3, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
