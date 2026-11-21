# regrasp at the rim: choose the top-layer point near (r 0.195, ang 108..114) with uv near the spine
w_ = zz_w(); P_ = w_.points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
L_ = P_[:, :2] - hc_; r_ = np.linalg.norm(L_, axis=1); a_ = np.degrees(np.arctan2(L_[:, 1], L_[:, 0]))
s_ = np.flatnonzero((r_ > 0.165) & (r_ < 0.205) & (a_ > 98) & (a_ < 122) & (P_[:, 2] > 0.5))
top_ = s_[np.argsort(-P_[s_, 2])[:10]]
for i_ in top_:
    print(int(i_), "r", round(float(r_[i_]), 3), "ang", round(float(a_[i_]), 1), "z", round(float(P_[i_, 2]), 3), "uv", np.round(U_[i_], 2).tolist(), flush=True)
zz_it = int(top_[0])
zz_ang = np.radians(float(a_[zz_it])); zz_tan = np.array([-np.sin(zz_ang), np.cos(zz_ang), 0.0])
zz_QR = {"right": q_(R_down(zz_tan))}
print("target particle", zz_it, np.round(P_[zz_it], 3).tolist(), "rf", np.round(zz_to_rf(P_[zz_it]), 3).tolist(), "tangent", np.round(zz_tan, 2).tolist(), flush=True)
PRE_ACTION("zz_regrasp_pre", {})
jaw_force["right"] = 20.0; jaw_target["right"] = 0.035
hp_ = pad_mid("right").copy()
r1_ = zz_pads_to("right", hp_, Q=zz_QR, speed=0.06, step=0.05)
r2_ = zz_pads_to("right", np.r_[P_[zz_it][:2], 0.78], Q=zz_QR, speed=0.08, step=0.06)
Rn_ = ts.ee_pose("right")[1]
print("above:", r2_, "fingers", np.round(Rn_[:, 0], 2).tolist(), "close", np.round(Rn_[:, 1], 2).tolist(), "gap", round(gap("right"), 3), "pelvis", state()["pelvis"], contact_report(), flush=True)
print("look", zz_look(P_[zz_it], "regrasp_above", dist=0.8, h=0.5, dirs=(60.0, 150.0, 240.0), top=True), flush=True)
