P_ = zz_w().points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
for u_ in (0.0, 0.04, 0.08, 0.12, 0.16, 0.20):
    row_ = []
    for v_ in (-0.2, -0.1, 0.0, 0.1, 0.2):
        i_ = int(np.argmin(np.linalg.norm(U_ - np.array([u_, v_]), axis=1)))
        L_ = P_[i_, :2] - hc_
        # is it on the surface of the bunch? count cloth points above it within 2.5 cm horizontally
        nr_ = np.flatnonzero((np.linalg.norm(P_[:, :2] - P_[i_, :2], axis=1) < 0.025) & (P_[:, 2] > P_[i_, 2] + 0.012))
        row_.append(f"[{i_} r{np.linalg.norm(L_):.3f} a{np.degrees(np.arctan2(L_[1], L_[0])):.0f} z{P_[i_,2]:.3f} above{len(nr_)}]")
    print(f"u {u_:+.2f}: " + " ".join(row_), flush=True)
print("v = -0.2, -0.1, 0, 0.1, 0.2; above = cloth points lying over it", flush=True)
