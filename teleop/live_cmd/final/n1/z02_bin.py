bn_ = body_of("rubbish_bin"); print("bin", np.round(centre(bn_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(bn_)], "tilt", round(box_tilt_deg(bn_), 1), flush=True)
for n_ in ("r195i3_paper", "r195i1_paper", "r149i1_pouch", "r158i1_tissue"):
    b_ = body_of(n_); print(n_, np.round(centre(b_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(b_)], "inside", inside(b_, bn_), flush=True)
print(close(os.path.join(TELE_DIR, "n1_bin_check.jpg"), np.array([0.6, 0.6, 1.4]), centre(bn_), "bin check"), flush=True)
