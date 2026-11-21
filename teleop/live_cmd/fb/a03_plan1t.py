def zz_plan1():
    global zz_P, zz_U, zz_c
    zz_P = zz_w().points(0); zz_U = zz_uv()
    own_ = garment_rect(zz_BL)
    zz_c = []
    for u_ in (-0.48, -0.44, -0.40, -0.38, -0.36):
        for v_ in (-0.2, -0.1, 0.0, 0.1, 0.2, 0.26):
            zz_c.append(int(np.argmin(np.linalg.norm(zz_U - np.array([u_, v_]), axis=1))))
    for zz_i in zz_c:
        pt_ = zz_P[zz_i]
        nr_ = np.linalg.norm(zz_P[:, :2] - pt_[:2], axis=1) < 0.03
        out_ = []
        for sd_ in ("right", "left"):
            for yr_ in (0.27, 0.31):
                g_, c_ = stance_for(np.r_[pt_[:2], 0.0], sd_, X_REL, yr_, ignore=(zz_BL,), with_cost=True, squat=True, clear_of=(own_,))
                out_.append((sd_[0], yr_, None if g_ is None else np.round(g_, 2).tolist()))
        print("pt", zz_i, "uv", np.round(zz_U[zz_i], 3).tolist(), "world", np.round(pt_, 3).tolist(), "relief", round(float(np.ptp(zz_P[nr_, 2])), 3), out_, flush=True)


with_tight(zz_plan1)
