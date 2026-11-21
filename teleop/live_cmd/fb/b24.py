PRE_ACTION("zz_fingers_down", {})
Rn_ = ts.ee_pose("right")[1]
print("fingers dir", np.round(Rn_[:, 0], 2).tolist(), "close dir", np.round(Rn_[:, 1], 2).tolist(), flush=True)
cd_ = Rn_[:, 1].copy(); cd_[2] = 0.0
if np.linalg.norm(cd_) < 0.3:
    cd_ = RM.rz(base()[1])[:, 1].copy()
cd_ /= np.linalg.norm(cd_)
zz_QD = {"right": q_(R_down(cd_))}
hp_ = pad_mid("right").copy()
r_ = zz_pads_to("right", hp_, Q=zz_QD, speed=0.06, step=0.05)
op.move({"right": ts.ee_pose("right")[0].tolist()}, speed=0.05, quats=zz_QD, timeout=4.0, tol=0.01); op.run(1.0)
Rn_ = ts.ee_pose("right")[1]
print("after: fingers dir", np.round(Rn_[:, 0], 2).tolist(), r_, "at_fingers", zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "top", round(float(zz_w().points(0)[:, 2].max()), 3), contact_report(), flush=True)
print("look", zz_look(np.array([-2.14, -1.85, 0.7]), "fingers_down", dist=1.3, h=0.8, dirs=(20.0, 160.0), top=True), flush=True)
