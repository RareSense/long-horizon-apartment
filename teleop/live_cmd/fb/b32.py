w_ = zz_w(); P_ = w_.points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
L_ = P_[:, :2] - hc_; r_ = np.linalg.norm(L_, axis=1); a_ = np.degrees(np.arctan2(L_[:, 1], L_[:, 0]))
print("asleep", w_.asleep, "blanket", in_container(zz_BL, zz_hb()), flush=True)
out_ = r_ > 0.262
print("outside n", int(out_.sum()), "ang range", round(float(a_[out_].min()), 0), round(float(a_[out_].max()), 0), "z range", round(float(P_[out_, 2].min()), 3), round(float(P_[out_, 2].max()), 3), flush=True)
for z0_ in (0.55, 0.50, 0.45, 0.40, 0.35, 0.30, 0.20, 0.10):
    s_ = np.flatnonzero(out_ & (np.abs(P_[:, 2] - z0_) < 0.025))
    if not len(s_):
        continue
    row_ = []
    for a0_ in range(80, 190, 10):
        k_ = s_[(a_[s_] >= a0_) & (a_[s_] < a0_ + 10)]
        if len(k_):
            i_ = k_[np.argmax(r_[k_])]
            row_.append(f"{a0_}:{r_[i_]-0.257:+.3f}/{r_[k_].min()-0.257:+.3f}({U_[i_,0]:+.2f},{U_[i_,1]:+.2f})")
    print(f"z {z0_:.2f}: " + " ".join(row_), flush=True)
print("(per 10 deg sector: outermost bulge / innermost [m from the outer wall] and uv of the outermost point)", flush=True)
print("pelvis", state()["pelvis"], "pelvis ang from hamper", round(float(np.degrees(np.arctan2(base()[0][1] - hc_[1], base()[0][0] - hc_[0]))), 1), flush=True)
p_, y_ = base()
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
cc_ = np.array([hc_[0] - 0.12, hc_[1] + 0.27, 0.42])
close(t_[0], np.array([p_[0], p_[1], 1.25]), cc_, "tail from the robot's head")
close(t_[1], cc_ + np.array([-0.7, 0.25, 0.25]), cc_, "tail from the west")
close(t_[2], cc_ + np.array([0.5, 0.45, 0.2]), cc_, "tail from the north-east")
print("look", zz_img(t_, "tail_outside"), flush=True)
