op.run(2.0)
w_ = zz_w(); P_ = w_.points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
print("asleep", w_.asleep, "blanket", in_container(zz_BL, zz_hb()), "top", round(float(P_[:, 2].max()), 3), flush=True)
for u_ in (-0.45, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
    row_ = []
    for v_ in (-0.3, -0.15, 0.0, 0.15, 0.3):
        i_ = int(np.argmin(np.linalg.norm(U_ - np.array([u_, v_]), axis=1)))
        r_ = float(np.linalg.norm(P_[i_, :2] - hc_))
        row_.append(f"({P_[i_,0]-hc_[0]:+.2f},{P_[i_,1]-hc_[1]:+.2f},{P_[i_,2]:.2f}{'i' if r_ < 0.235 else 'o'})")
    print(f"u {u_:+.2f}: " + " ".join(row_), flush=True)
print("(x east, y north of the hamper centre, z; i = inside the footprint) for v = -0.3, -0.15, 0, 0.15, 0.3", flush=True)
