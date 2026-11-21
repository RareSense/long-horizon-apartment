bn_ = body_of("rubbish_bin"); rc_ = obj_rect("rubbish_bin")
print("rec", rec.n, "state", state(), "done", len(DONE), flush=True)
print("bin c", np.round(centre(bn_), 3).tolist(), "rect c", np.round(rc_.c, 3).tolist(), "h", np.round(rc_.h, 3).tolist(), "R", np.round(rc_.R, 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), flush=True)
for n_ in ("r195i3_paper", "r195i1_paper", "r149i1_pouch", "r158i1_tissue"):
    b_ = body_of(n_); c_ = centre(b_); lo_, hi_ = obj_box(b_)
    print(n_, "c", np.round(c_, 3).tolist(), "in bin frame", np.round((c_[:2] - rc_.c) @ rc_.R, 3).tolist(), "size", np.round(hi_ - lo_, 3).tolist(), "inside", inside(b_, bn_), flush=True)
print(close(os.path.join(TELE_DIR, "x00_bin_top.jpg"), centre(bn_) + np.array([0.05, -0.05, 1.3]), centre(bn_), "bin top"), flush=True)
print(look3("x00_bin"), flush=True)
