w_ = zz_w(); P_ = w_.points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
L_ = P_[:, :2] - hc_; r_ = np.linalg.norm(L_, axis=1); a_ = np.degrees(np.arctan2(L_[:, 1], L_[:, 0]))
print("asleep", w_.asleep, "blanket", in_container(zz_BL, zz_hb()), flush=True)
for band_ in ((0.12, 0.16), (0.16, 0.20), (0.20, 0.235)):
    s_ = np.flatnonzero((r_ >= band_[0]) & (r_ < band_[1]) & (P_[:, 2] > 0.40))
    # the top surface: per 6 deg sector, the highest point
    print("band r", band_, "n", len(s_), flush=True)
    for a0_ in range(60, 200, 6):
        k_ = s_[(a_[s_] >= a0_) & (a_[s_] < a0_ + 6)]
        if len(k_):
            i_ = k_[np.argmax(P_[k_, 2])]
            print(f"   ang {a0_:3d}: top z {P_[i_,2]:.3f} uv ({U_[i_,0]:+.2f},{U_[i_,1]:+.2f}) n {len(k_)}  zs {np.round(np.sort(P_[k_,2])[-4:],2).tolist()}", flush=True)
print("pad size", np.round(m.geom_size[m.geom("right_Dex1_finger_link_1_pad").id], 4).tolist(), "handles: hamper box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_hb())], flush=True)
cc_ = np.r_[hc_, 0.6]
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.05, 0.10, 0.75]), cc_ + np.array([-0.08, 0.10, 0.0]), "rim crossing top")
close(t_[1], cc_ + np.array([-0.55, 0.55, 0.45]), cc_ + np.array([-0.1, 0.12, -0.05]), "rim crossing from NW")
close(t_[2], cc_ + np.array([0.35, -0.45, 0.50]), cc_ + np.array([-0.1, 0.12, -0.05]), "rim crossing from SE (inside)")
print("look", zz_img(t_, "rim_crossing"), flush=True)
