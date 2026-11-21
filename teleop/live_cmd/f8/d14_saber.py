zz_sb = body_of("r130i1_light_saber"); zid_ = m.body(zz_sb).id
print("saber", zz_sb, "mass", round(float(m.body_mass[zid_]), 3), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_sb)], "dest", DESC["destinations"].get("r130i1_light_saber"), flush=True)
P_ = piece_points(zz_sb)
for k_, V_ in P_.items():
    c_ = V_.mean(0); X_ = V_[:, :2] - c_[:2]; w_, U_ = np.linalg.eigh(X_.T @ X_); ax_ = U_[:, -1]; s_ = X_ @ ax_; t_ = X_ @ np.array([-ax_[1], ax_[0]])
    print(" piece", k_, "c", np.round(c_, 3).tolist(), "axis", np.round(ax_, 3).tolist(), "len", round(float(np.ptp(s_)), 3), "width", round(float(np.ptp(t_)), 3), "z", round(float(V_[:, 2].min()), 3), round(float(V_[:, 2].max()), 3), flush=True)
print("scooter", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], scooter_parts(zz_s)["deck"], flush=True)
