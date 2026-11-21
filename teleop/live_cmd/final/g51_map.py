# read only: cross-sections of the hanging coat in the robot frame, and the outside parts by wing (AI-operated)
def zz_raster2(zc, dz=0.011):
    P_ = zz_w().points(0); U_ = zz_uv()
    s_ = np.flatnonzero(np.abs(P_[:, 2] - zc) < dz)
    B_ = np.array([zz_to_rf(P_[i_]) for i_ in s_])
    x0_, x1_ = 0.24, 0.56; y0_, y1_ = -0.26, 0.10
    nx_ = int(round((x1_ - x0_) / 0.01)); ny_ = int(round((y1_ - y0_) / 0.01))
    G_ = [[" ." for _ in range(ny_)] for _ in range(nx_)]
    for k_, i_ in enumerate(s_):
        ix_ = int((B_[k_, 0] - x0_) / 0.01); iy_ = int((y1_ - B_[k_, 1]) / 0.01)
        if 0 <= ix_ < nx_ and 0 <= iy_ < ny_:
            G_[ix_][iy_] = "%+d" % int(np.clip(round(U_[i_, 0] * 10), -8, 8)) if abs(U_[i_, 0]) >= 0.05 else " 0"
    print(f"--- z {zc}: n {len(s_)}  v range {U_[s_, 1].min():.2f}..{U_[s_, 1].max():.2f}; rows = ahead x (far at top), columns = y +0.10 (left) .. -0.26 (right); cell = u*10 (the coat's LONG coordinate)", flush=True)
    for ix_ in range(nx_ - 1, -1, -1):
        print(f"{x0_ + ix_ * 0.01:5.2f} " + "".join(G_[ix_]), flush=True)


for z_ in (0.70, 0.78, 0.88):
    zz_raster2(z_)
P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb())
B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); rr_ = np.linalg.norm(P_[:, :2] - hc_, axis=1)
o_ = rr_ > hr_
for nm_, s_ in (("wing u>0.1", U_[:, 0] > 0.1), ("middle |u|<0.1", np.abs(U_[:, 0]) <= 0.1), ("wing u<-0.1", U_[:, 0] < -0.1)):
    k_ = o_ & s_
    if k_.any():
        print(nm_, "outside n", int(k_.sum()), "uv lo/hi", np.round(U_[k_].min(0), 2).tolist(), np.round(U_[k_].max(0), 2).tolist(), "z", round(float(P_[k_, 2].min()), 3), round(float(P_[k_, 2].max()), 3), "rf lo/hi", np.round(B_[k_].min(0), 3).tolist(), np.round(B_[k_].max(0), 3).tolist(), flush=True)
print("grid: rows u, columns v (0.39, 0.3, 0.2, 0.1, 0, -0.2, -0.39); cell = rf x y z, r", flush=True)
for u_ in (-0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8):
    row_ = []
    for v_ in (0.39, 0.3, 0.2, 0.1, 0.0, -0.2, -0.39):
        i_ = int(np.argmin(np.linalg.norm(U_ - np.array([u_, v_]), axis=1)))
        row_.append(f"[{B_[i_,0]:.2f} {B_[i_,1]:+.2f} {B_[i_,2]:.2f} r{rr_[i_]:.2f}]")
    print(f"u {u_:+.1f}: " + " ".join(row_), flush=True)
for z_ in (0.70, 0.74, 0.78, 0.82, 0.86, 0.90):
    s_ = np.flatnonzero(np.abs(P_[:, 2] - z_) < 0.012); i_n = s_[np.argmin(B_[s_, 0])]
    print("z", z_, "nearest", int(i_n), np.round(B_[i_n], 3).tolist(), "uv", np.round(U_[i_n], 2).tolist(), flush=True)
