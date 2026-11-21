# left hold back up over the opening (the first end comes off the rim fold), then map the cloth at the north rim (AI-operated)
PRE_ACTION("zz_left_up", {})
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.06, step=0.05)
    print("left to", zz_t, zz_r, "held L", cloth_held("left"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "knees", zz_knees(), "fell", fallen(), flush=True)
op.run(1.0)


def zz_rimmap(z0=0.60, z1=0.80):
    P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb())
    B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_])
    x0_, x1_ = 0.22, 0.44; y0_, y1_ = -0.26, 0.06
    nx_ = int(round((x1_ - x0_) / 0.01)); ny_ = int(round((y1_ - y0_) / 0.01))
    top_ = {}
    for i_ in np.flatnonzero((B_[:, 2] > z0) & (B_[:, 2] < z1)):
        ix_ = int((B_[i_, 0] - x0_) / 0.01); iy_ = int((y1_ - B_[i_, 1]) / 0.01)
        if 0 <= ix_ < nx_ and 0 <= iy_ < ny_ and (top_.get((ix_, iy_)) is None or B_[i_, 2] > B_[top_[(ix_, iy_)], 2]):
            top_[(ix_, iy_)] = i_
    print(f"top cloth point per 1 cm cell, {z0} < z < {z1}: letter F far end (u>0.3) / m middle / e first end (u<-0.3), digit = cm above the rim; rows = ahead x (far at top), columns y +0.06 .. -0.26; # = wall", flush=True)
    for ix_ in range(nx_ - 1, -1, -1):
        row_ = ""
        for iy_ in range(ny_):
            xx_ = x0_ + (ix_ + 0.5) * 0.01; yy_ = y1_ - (iy_ + 0.5) * 0.01
            rr_ = float(np.linalg.norm(zz_rf((xx_, yy_, 0.0))[:2] - hc_))
            i_ = top_.get((ix_, iy_))
            if i_ is None:
                row_ += " #" if abs(rr_ - hr_ + 0.01) < 0.012 else " ."
            else:
                row_ += ("F" if U_[i_, 0] > 0.3 else ("e" if U_[i_, 0] < -0.3 else "m")) + str(min(9, int(round((B_[i_, 2] - 0.59) * 100))))
        print(f"{x0_ + ix_ * 0.01:5.2f} " + row_, flush=True)


zz_rimmap()
print("fold target", bc_fold_target(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "inside", in_container(zz_BL, zz_hb()), flush=True)
P_ = zz_w().points(0); U_ = zz_uv(); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_])
for uv_ in ((-0.5, 0.0), (-0.44, 0.0), (-0.5, 0.2), (-0.5, -0.2), (0.4, -0.14), (0.46, -0.14), (0.5, -0.14), (0.42, -0.18), (0.4, -0.3), (0.5, -0.375)):
    i_ = int(np.argmin(np.linalg.norm(U_ - np.array(uv_), axis=1)))
    print("uv", uv_, "idx", i_, "rf", np.round(B_[i_], 3).tolist(), flush=True)
print("pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "pelvis", state()["pelvis"], flush=True)
cc_ = zz_rf((0.33, -0.11, 0.68))
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.55, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.3, 0.3]), cc_, "from the south-west")
print("look", zz_img(t_, "g17_lup"), flush=True)
