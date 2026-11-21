zz_o = "left"
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
zz_QL = {zz_o: q_(zz_R(-zz_lat, zz_fwd))}
PRE_ACTION("zz_left_pre", {})
jaw_force[zz_o] = 20.0; jaw_target[zz_o] = 0.038; op.run(0.3)
for zz_t in ((0.25, 0.30, 0.60), (0.36, 0.28, 0.77)):
    zz_r = zz_pads_to(zz_o, zz_rf(zz_t), Q=zz_QL, speed=0.10)
    Rn_ = ts.ee_pose(zz_o)[1]
    print("left to", zz_t, zz_r, "fingers dir rf", np.round(RM.rz(y_).T @ Rn_[:, 0], 2).tolist(), "close dir rf", np.round(RM.rz(y_).T @ Rn_[:, 1], 2).tolist(), "gap", round(gap(zz_o), 3), contact_report(), flush=True)
zz_P = zz_w().points(0)
print("C rf", np.round(zz_to_rf(zz_P[994]), 3).tolist(), "state", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), flush=True)
print("look", zz_look(zz_P[994], "left_pre", dist=0.9, h=0.3, dirs=(120.0, 210.0, 30.0, 75.0)), flush=True)
