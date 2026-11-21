P_ = zz_w().points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
for uv_ in ((0.02, 0.24), (0.04, 0.26), (0.04, 0.30), (0.06, 0.28), (0.08, 0.32), (0.10, 0.30), (0.0, 0.2)):
    i_ = int(np.argmin(np.linalg.norm(U_ - np.array(uv_), axis=1)))
    L_ = P_[i_, :2] - hc_
    k_ = np.flatnonzero((np.linalg.norm(P_[:, :2] - P_[i_, :2], axis=1) < 0.02))
    print("uv", uv_, "idx", i_, "rel", np.round(L_, 3).tolist(), "r", round(float(np.linalg.norm(L_)), 3), "z", round(float(P_[i_, 2]), 3), "top z here", round(float(P_[k_, 2].max()), 3), "rf", np.round(zz_to_rf(P_[i_]), 3).tolist(), flush=True)
zz_it2 = int(np.argmin(np.linalg.norm(U_ - np.array(ZZ_UV2), axis=1)))
p_, y_ = base(); zz_lat = RM.rz(y_)[:, 1]
zz_QRD = {"right": q_(R_down(zz_lat))}
PRE_ACTION("zz_right_pre2", {})
jaw_force["right"] = 20.0; jaw_target["right"] = 0.036
tg_ = P_[zz_it2].copy()
for zz_t in (np.r_[tg_[:2] + np.array([0.0, 0.10]), 1.0], np.r_[tg_[:2], 0.86]):
    zz_r = zz_pads_to("right", zz_t, Q=zz_QRD, speed=0.08, step=0.06)
    Rn_ = ts.ee_pose("right")[1]
    print("right to", np.round(zz_t, 3).tolist(), zz_r, "fingers", np.round(Rn_[:, 0], 2).tolist(), "close", np.round(Rn_[:, 1], 2).tolist(), "at_fingers R", zz_w().at_fingers("right"), "touch", contact_report(), "knees", {k_: v_[0] for k_, v_ in zz_knees().items() if "knee" in k_}, flush=True)
print("target", zz_it2, np.round(zz_w().points(0)[zz_it2], 3).tolist(), "in_pads", zz_in_pads("right", zz_it2), "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "blanket", in_container(zz_BL, zz_hb()), flush=True)
cc_ = zz_w().points(0)[zz_it2]
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.6, 0.35, 0.3]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.7]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.4, 0.3]), cc_, "from the south-west")
print("look", zz_img(t_, "right_pre2"), flush=True)
