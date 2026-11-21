zz_o = "left"; zz_it = 1150
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
zz_QL = {zz_o: q_(zz_R(-zz_lat, zz_fwd))}
PRE_ACTION("zz_left_pre", {})
jaw_force[zz_o] = 20.0; jaw_target[zz_o] = 0.038; op.run(0.3)
P_ = zz_w().points(0)
for zz_t in ((0.25, 0.30, 0.62), (0.36, 0.22, float(P_[zz_it][2]))):
    zz_r = zz_pads_to(zz_o, zz_rf(zz_t), Q=zz_QL, speed=0.10)
    Rn_ = ts.ee_pose(zz_o)[1]
    print("left to", np.round(zz_t, 3).tolist(), zz_r, "fingers rf", np.round(RM.rz(y_).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(y_).T @ Rn_[:, 1], 2).tolist(), "gap", round(gap(zz_o), 3), contact_report(), "pelvis", state()["pelvis"], flush=True)
print("target", zz_it, np.round(zz_w().points(0)[zz_it], 3).tolist(), "in_pads", zz_in_pads(zz_o, zz_it), "right held", cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), flush=True)
cc_ = np.array([-2.20, -1.78, 0.75])
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.6, -0.45, 0.25]), cc_, "from the south-east")
close(t_[1], cc_ + np.array([0.05, 0.02, 0.8]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.2, 0.75, 0.3]), cc_, "from the north")
print("look", zz_img(t_, "left_pre2"), flush=True)
