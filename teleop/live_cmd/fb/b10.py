# turn the holding (right) gripper about the vertical: the bunch turns with it
def zz_ridge_dir():
    P_ = zz_w().points(0); zc_ = float(P_[994][2])
    s_ = np.abs(P_[:, 2] - zc_) < 0.03
    cen_ = np.array([zz_to_rf(p_) for p_ in P_[s_]])[:, :2].mean(0)
    c_ = zz_to_rf(P_[994])[:2]
    return round(float(np.degrees(np.arctan2(c_[1] - cen_[1], c_[0] - cen_[0]))), 1), np.round(c_ - cen_, 3).tolist(), np.round(c_, 3).tolist()
Rn_ = ts.ee_pose(zz_sd)[1]; p_, y_ = base()
cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_)
print("right fingers dir", np.round(Rn_[:, 0], 2).tolist(), "close dir rf deg", round(float(np.degrees(np.arctan2(cd_[1], cd_[0]) - y_)), 1), "ridge", zz_ridge_dir(), flush=True)
zz_hold = pad_mid(zz_sd).copy()
for zz_a in ZZ_ANGLES:
    PRE_ACTION("zz_turn_bunch", dict(angle=zz_a))
    c2_ = RM.rz(np.radians(zz_a)) @ cd_
    zz_QR = {zz_sd: q_(R_down(c2_))}
    hp_ = ts.ee_pose(zz_sd)[0]
    op.move({zz_sd: hp_.tolist()}, speed=0.05, quats=zz_QR, timeout=4.0, tol=0.01); op.run(0.5)
    zz_r = zz_pads_to(zz_sd, zz_hold, Q=zz_QR, speed=0.05, step=0.05)
    op.run(2.5)
    Rn2_ = ts.ee_pose(zz_sd)[1]; c3_ = Rn2_[:, 1].copy()
    print("turn", zz_a, "achieved deg", round(float(np.degrees(np.arctan2(c3_[1], c3_[0]) - np.arctan2(cd_[1], cd_[0]))), 1), "fingers", np.round(Rn2_[:, 0], 2).tolist(), zz_r, "ridge", zz_ridge_dir(), "held", cloth_held(zz_sd), contact_report(), flush=True)
print("look", zz_look(zz_w().points(0)[994], "bunch_turned", dist=0.9, h=0.3, dirs=(120.0, 210.0, 30.0), top=True), flush=True)
