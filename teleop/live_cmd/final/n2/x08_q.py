pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin"); rc_ = obj_rect(bn_)
P_ = GG.body_points(m, d, m.body(pb_).id); q_l = (P_[:, :2] - rc_.c) @ rc_.R
print("npts", len(P_), "bin c", np.round(rc_.c, 3).tolist(), "h", np.round(rc_.h, 3).tolist(), "R", np.round(rc_.R, 3).tolist(), flush=True)
print("paper pts in bin frame min", np.round(q_l.min(0), 3).tolist(), "max", np.round(q_l.max(0), 3).tolist(), "z", round(float(P_[:, 2].min()), 3), round(float(P_[:, 2].max()), 3), flush=True)
pr_ = paper_rect = obj_rect(pb_); print("paper rect c", np.round(pr_.c, 3).tolist(), "h", np.round(pr_.h, 3).tolist(), "R", np.round(pr_.R, 3).tolist(), "flat_corners", np.round(flat_corners(pb_)[0], 3).tolist(), flush=True)
print(close(os.path.join(TELE_DIR, "x08_paper1_top.jpg"), centre(pb_) + np.array([0.02, 0.02, 0.7]), centre(pb_), "paper r195i1"), flush=True)
