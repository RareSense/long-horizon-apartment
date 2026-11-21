w_ = zz_w(); P_ = w_.points(0)
i_ = np.argsort(-P_[:, 2])[:12]
a_, b_ = pads("right")
print("pads", np.round(a_, 3).tolist(), np.round(b_, 3).tolist(), "gap", round(gap("right"), 3), flush=True)
for k_ in i_:
    print(int(k_), np.round(P_[k_], 3).tolist(), "uv", np.round(zz_uv()[k_], 2).tolist(), "in_pads", zz_in_pads("right", int(k_)), flush=True)
print("holds", list(w_.holds.keys()), "LOCK", {s_: len(v_[1]) for s_, v_ in LOCK.items()}, "SQ", list(SQ.keys()), flush=True)
c_ = pad_mid("right")
p_, y_ = base(); Rz_ = RM.rz(y_)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], c_ + Rz_ @ np.array([0.05, -0.30, 0.05]), c_ - [0, 0, 0.03], "finger from the right")
close(t_[1], c_ + Rz_ @ np.array([0.30, 0.0, 0.08]), c_ - [0, 0, 0.03], "finger from ahead")
close(t_[2], c_ + Rz_ @ np.array([0.05, 0.30, 0.05]), c_ - [0, 0, 0.03], "finger from the left")
print("look", zz_img(t_, "hooked_close"), flush=True)
