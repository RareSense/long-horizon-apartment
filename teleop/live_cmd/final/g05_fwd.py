# one small move of the open left jaws straight ahead into the fold (AI-operated)
PRE_ACTION("zz_fwd", dict(d=ZZ_D))
p_, y_ = base(); mv_ = RM.rz(y_) @ np.asarray(ZZ_D, float)
hp_ = ts.ee_pose(zz_o)[0]
op.move({zz_o: (hp_ + mv_).tolist()}, speed=0.04, quats=zz_QF, timeout=3.0, tol=0.006); op.run(0.3)
a_, b_ = pads(zz_o); cg_ = zz_w().caught(zz_o)
print("pad rf", np.round(zz_to_rf(pad_mid(zz_o)), 3).tolist(), "pads rf", np.round(zz_to_rf(a_), 3).tolist(), np.round(zz_to_rf(b_), 3).tolist(), "caught", len(cg_), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None,
      "at_f", zz_w().at_fingers(zz_o), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "fell", fallen(), flush=True)
P_ = zz_w().points(0); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); U_ = zz_uv()
pm_ = zz_to_rf(pad_mid(zz_o))
s_ = np.flatnonzero((np.abs(B_[:, 2] - pm_[2]) < 0.02) & (np.abs(B_[:, 0] - pm_[0]) < 0.05) & (np.abs(B_[:, 1] - pm_[1]) < 0.07))
for i_ in s_[np.argsort(B_[s_, 1])]:
    print("   near", int(i_), "rel pad (ahead, left, up)", np.round(B_[i_] - pm_, 3).tolist(), "uv", np.round(U_[i_], 2).tolist(), flush=True)
print("right held", cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), flush=True)
cc_ = pad_mid(zz_o)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.5, 0.2, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.55]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, 0.2, 0.2]), cc_, "from the west")
print("look", zz_img(t_, "g05_fwd"), flush=True)
