# cross-sections of the hanging blanket in the robot frame (AI-operated; read only)
def zz_raster(zc, dz=0.011):
    P_ = zz_w().points(0); U_ = zz_uv()
    s_ = np.flatnonzero(np.abs(P_[:, 2] - zc) < dz)
    B_ = np.array([zz_to_rf(P_[i_]) for i_ in s_])
    x0_, x1_ = 0.24, 0.56; y0_, y1_ = -0.26, 0.10
    nx_ = int(round((x1_ - x0_) / 0.01)); ny_ = int(round((y1_ - y0_) / 0.01))
    G_ = [[" ." for _ in range(ny_)] for _ in range(nx_)]
    for k_, i_ in enumerate(s_):
        ix_ = int((B_[k_, 0] - x0_) / 0.01); iy_ = int((y1_ - B_[k_, 1]) / 0.01)
        if 0 <= ix_ < nx_ and 0 <= iy_ < ny_:
            G_[ix_][iy_] = "%+d" % int(round(U_[i_, 1] * 10)) if abs(U_[i_, 1]) >= 0.05 else " 0"
    print(f"--- z {zc}: n {len(s_)}  u range {U_[s_, 0].min():.2f}..{U_[s_, 0].max():.2f}; rows = ahead x (far at top), columns = y from +0.10 (left) to -0.26 (right); cell = v*10", flush=True)
    for ix_ in range(nx_ - 1, -1, -1):
        print(f"{x0_ + ix_ * 0.01:5.2f} " + "".join(G_[ix_]), flush=True)


for z_ in (0.70, 0.76, 0.84, 0.92):
    zz_raster(z_)
# the near edge (toward the robot) and the left edge of the strand per height
P_ = zz_w().points(0); U_ = zz_uv()
B_ = np.array([zz_to_rf(p_) for p_ in P_])
for z_ in (0.66, 0.70, 0.74, 0.78, 0.82, 0.86, 0.90, 0.95):
    s_ = np.flatnonzero(np.abs(P_[:, 2] - z_) < 0.012)
    i_n = s_[np.argmin(B_[s_, 0])]; i_l = s_[np.argmax(B_[s_, 1])]
    print("z", z_, "nearest", int(i_n), np.round(B_[i_n], 3).tolist(), "uv", np.round(U_[i_n], 2).tolist(), "| leftmost", int(i_l), np.round(B_[i_l], 3).tolist(), "uv", np.round(U_[i_l], 2).tolist(), flush=True)
print("left shoulder rf", np.round(zz_to_rf(d.xpos[m.body("left_shoulder_pitch_link").id]), 3).tolist(), "torso tilt", round(pelvis_tilt(), 3), flush=True)
