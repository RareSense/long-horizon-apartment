w_ = zz_w(); P_ = w_.points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
L_ = P_[:, :2] - hc_; r_ = np.linalg.norm(L_, axis=1); a_ = np.degrees(np.arctan2(L_[:, 1], L_[:, 0]))
print("asleep", w_.asleep, "blanket", in_container(zz_BL, zz_hb()), "rim top z:", round(float(obj_box(zz_hb())[1][2]) - 0.08, 3), flush=True)
for band_ in ((0.20, 0.228), (0.228, 0.262)):
    s_ = np.flatnonzero((r_ >= band_[0]) & (r_ < band_[1]) & (P_[:, 2] > 0.50))
    print("band r", band_, "n", len(s_), flush=True)
    for a0_ in range(84, 180, 4):
        k_ = s_[(a_[s_] >= a0_) & (a_[s_] < a0_ + 4)]
        if len(k_):
            o_ = k_[np.argsort(-P_[k_, 2])]
            print(f"   ang {a0_:3d}: " + " ".join(f"[{int(i_)} z{P_[i_,2]:.3f} r{r_[i_]:.3f} uv({U_[i_,0]:+.2f},{U_[i_,1]:+.2f})]" for i_ in o_[:3]), flush=True)
