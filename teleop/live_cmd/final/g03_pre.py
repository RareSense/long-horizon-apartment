# left hand, fingers AHEAD and jaws closing across the body, to a pre-position in front of the strand's near fold (AI-operated)
zz_o = "left"
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
zz_QF = {zz_o: q_(zz_R(zz_fwd, zz_lat))}
print("JAW_OPEN", JAW_OPEN, "PRE_OPEN", PRE_OPEN, "gap now", round(gap(zz_o), 4), flush=True)
PRE_ACTION("zz_left_pre", {})
jaw_force[zz_o] = 20.0; jaw_target[zz_o] = JAW_OPEN; op.run(0.4)
print("gap open", round(gap(zz_o), 4), "jaw", round(float(jaw(zz_o)), 4), flush=True)
for zz_t in ZZ_PRE:
    zz_r = zz_pads_to(zz_o, zz_rf(zz_t), Q=zz_QF, speed=0.10, step=0.06)
    Rn_ = ts.ee_pose(zz_o)[1]; a_, b_ = pads(zz_o)
    print("left to", zz_t, zz_r, "fingers rf", np.round(RM.rz(y_).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(y_).T @ Rn_[:, 1], 2).tolist(), "pads rf", np.round(zz_to_rf(a_), 3).tolist(), np.round(zz_to_rf(b_), 3).tolist(),
          "caught", len(zz_w().caught(zz_o)), "at_f", zz_w().at_fingers(zz_o), contact_report(), "knees", zz_knees(), "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0:
        break
print("right held", cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), "pelvis", state()["pelvis"], flush=True)
P_ = zz_w().points(0); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); U_ = zz_uv()
for z_ in (0.72, 0.76, 0.80, 0.84):
    s_ = np.flatnonzero(np.abs(P_[:, 2] - z_) < 0.012); i_n = s_[np.argmin(B_[s_, 0])]
    print("z", z_, "nearest", int(i_n), np.round(B_[i_n], 3).tolist(), "uv", np.round(U_[i_n], 2).tolist(), flush=True)
cc_ = pad_mid(zz_o) + 0.08 * zz_fwd
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.55, 0.25, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.55, 0.25, 0.2]), cc_, "from the west")
print("look", zz_img(t_, "g03_pre"), flush=True)
