P_ = zz_w().points(0); U_ = zz_uv()
zc_ = ZZ_Z
s_ = np.flatnonzero(np.abs(P_[:, 2] - zc_) < 0.011)
X_ = P_[s_, :2]; c_ = X_.mean(0)
print("slab z", zc_, "n", len(s_), "centroid", np.round(c_, 3).tolist(), flush=True)
# text raster: 1 cm cells, x to the right (east), y up (north); cell shows the v-coordinate sign/size
x0_, x1_ = X_[:, 0].min() - 0.01, X_[:, 0].max() + 0.01; y0_, y1_ = X_[:, 1].min() - 0.01, X_[:, 1].max() + 0.01
nx_ = int(np.ceil((x1_ - x0_) / 0.01)); ny_ = int(np.ceil((y1_ - y0_) / 0.01))
G_ = [[" ." for _ in range(nx_)] for _ in range(ny_)]
for k_, i_ in enumerate(s_):
    ix_ = int((X_[k_, 0] - x0_) / 0.01); iy_ = int((X_[k_, 1] - y0_) / 0.01)
    v_ = U_[i_, 1]
    G_[iy_][ix_] = ("%+d" % int(round(v_ * 10))) if abs(v_) >= 0.05 else " 0"
for iy_ in range(ny_ - 1, -1, -1):
    print(f"{y0_ + iy_ * 0.01:6.2f} " + "".join(G_[iy_]), flush=True)
print("x from", round(x0_, 3), "to", round(x1_, 3), "(1 cm cells; number = v*10 of the particle there; 0 = the sheet's long midline)", flush=True)
print("u range in slab", round(float(U_[s_, 0].min()), 2), round(float(U_[s_, 0].max()), 2), "left pad rf", np.round(zz_to_rf(pad_mid("left")), 3).tolist(), flush=True)
