op.run(1.5)
P_ = zz_w().points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
L_ = P_[:, :2] - hc_; r_ = np.linalg.norm(L_, axis=1)
out_ = r_ > 0.257
print("blanket", in_container(zz_BL, zz_hb()), "outside n", int(out_.sum()), "uv lo/hi", np.round(U_[out_].min(0), 2).tolist(), np.round(U_[out_].max(0), 2).tolist(), "z lo", round(float(P_[out_, 2].min()), 3), "left pad", np.round(pad_mid("left"), 3).tolist(), flush=True)
# top-layer map (3 cm cells) over the north-west part: rows y (north at the top), cols x (west to east); cell: top z in cm above the rim, and u*100
xs_ = np.arange(-0.33, 0.07, 0.03); ys_ = np.arange(0.30, -0.10, -0.03)
print("cols x (rel. to the hamper centre):", " ".join(f"{x_:+.2f}" for x_ in xs_), flush=True)
for y_ in ys_:
    row_ = []
    for x_ in xs_:
        k_ = np.flatnonzero((np.abs(L_[:, 0] - x_) < 0.015) & (np.abs(L_[:, 1] - y_) < 0.015))
        if len(k_):
            i_ = k_[np.argmax(P_[k_, 2])]
            row_.append(f"{int(round((P_[i_,2]-0.59)*100)):+3d}/{int(round(U_[i_,0]*100)):+3d},{int(round(U_[i_,1]*100)):+3d}")
        else:
            row_.append("     .     ")
    print(f"y {y_:+.2f}: " + " ".join(row_), flush=True)
print("cell: top z [cm above the rim] / u*100, v*100 of the top particle; wall at r 0.235..0.257", flush=True)
