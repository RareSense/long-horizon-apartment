P_ = zz_w().points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
L_ = P_[:, :2] - hc_
xs_ = np.arange(-0.31, -0.13, 0.015); ys_ = np.arange(0.285, 0.14, -0.015)
print("cols x:", " ".join(f"{x_:+.3f}" for x_ in xs_), flush=True)
for y_ in ys_:
    row_ = []
    for x_ in xs_:
        k_ = np.flatnonzero((np.abs(L_[:, 0] - x_) < 0.0075) & (np.abs(L_[:, 1] - y_) < 0.0075))
        if len(k_):
            i_ = k_[np.argmax(P_[k_, 2])]
            row_.append(f"{int(round((P_[i_,2]-0.59)*100)):+3d}/{int(round(U_[i_,0]*100)):+3d},{int(round(U_[i_,1]*100)):+3d}")
        else:
            row_.append("     .     ")
    print(f"y {y_:+.3f}: " + " ".join(row_), flush=True)
print("pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "right pad", np.round(pad_mid("right"), 3).tolist(), "knees", {k_: v_[0] for k_, v_ in zz_knees().items() if "knee" in k_}, flush=True)
cc_ = np.r_[hc_ + np.array([-0.22, 0.22]), 0.68]
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.6, 0.35, 0.3]), cc_, "cliff from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.7]), cc_, "cliff from above")
close(t_[2], cc_ + np.array([-0.15, 0.7, 0.35]), cc_, "cliff from the north")
print("look", zz_img(t_, "cliff"), flush=True)
