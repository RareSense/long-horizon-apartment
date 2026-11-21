for n_ in ("r133i1_laundry_basket", "r193i1_toy_piece", "r193i2_toy_piece", "r193i3_toy_piece", "r193i4_toy_piece", "r192i1_ball", "r132i1_heater"):
    b_ = body_of(n_)
    if b_ is None: print(n_, None); continue
    lo_, hi_ = obj_box(b_); print(n_, np.round(centre(b_)[:2], 3).tolist(), "box", np.round(lo_[:2], 2).tolist(), np.round(hi_[:2], 2).tolist(), round(float(hi_[2]), 2), flush=True)
print("stock pts", [np.round(p_, 3).tolist() for p_ in cloth_grasp_points("r190i1_stocking", k=5, sep=0.05)], flush=True)
