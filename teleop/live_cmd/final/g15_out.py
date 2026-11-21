# read only: what is outside the wall now, by sheet region (AI-operated)
P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb())
B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_])
rr_ = np.linalg.norm(P_[:, :2] - hc_, axis=1)
o_ = rr_ > hr_
print("outside n", int(o_.sum()), "below rim outside", int((o_ & (P_[:, 2] < bc_rim(zz_hb()))).sum()), flush=True)
for nm_, s_ in (("far end u>0.3", U_[:, 0] > 0.3), ("middle -0.3<u<0.3", np.abs(U_[:, 0]) <= 0.3), ("first end u<-0.3", U_[:, 0] < -0.3)):
    k_ = o_ & s_
    if k_.any():
        print(" ", nm_, "outside n", int(k_.sum()), "uv lo/hi", np.round(U_[k_].min(0), 2).tolist(), np.round(U_[k_].max(0), 2).tolist(), "z lo/hi", round(float(P_[k_, 2].min()), 3), round(float(P_[k_, 2].max()), 3),
              "rf lo/hi", np.round(B_[k_].min(0), 3).tolist(), np.round(B_[k_].max(0), 3).tolist(), "r max", round(float(rr_[k_].max()), 3), flush=True)
    else:
        print(" ", nm_, "nothing outside", flush=True)
for uv_ in ((0.5, -0.375), (0.5, -0.2), (0.5, 0.0), (0.5, 0.375), (0.4, -0.375), (0.3, -0.375), (0.4, -0.16), (-0.5, 0.0), (-0.5, -0.375), (-0.5, 0.375), (-0.43, 0.16), (0.05, 0.2)):
    i_ = int(np.argmin(np.linalg.norm(U_ - np.array(uv_), axis=1)))
    print("uv", uv_, "idx", i_, "rf", np.round(B_[i_], 3).tolist(), "r", round(float(rr_[i_]), 3), flush=True)
for s_ in SIDES:
    a_, b_ = pads(s_); Rn_ = ts.ee_pose(s_)[1]
    print(s_, "pad rf", np.round(zz_to_rf(pad_mid(s_)), 3).tolist(), "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 1], 2).tolist(), "pad r from hamper", [round(float(np.linalg.norm(x_[:2] - hc_)), 3) for x_ in (a_, b_)], flush=True)
print("inside", in_container(zz_BL, zz_hb()), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
