P_ = zz_w().points(0); hc_ = obj_rect(zz_hb()).c; U_ = zz_uv()
L_ = P_[:, :2] - hc_; r_ = np.linalg.norm(L_, axis=1); a_ = np.degrees(np.arctan2(L_[:, 1], L_[:, 0]))
o_ = r_ > 0.257
print("outside", int(o_.sum()), "ang", np.round(np.percentile(a_[o_], [0, 25, 50, 75, 100]), 0).tolist(), "r max", round(float(r_[o_].max()), 3), "z", np.round(np.percentile(P_[o_, 2], [0, 50, 100]), 3).tolist(), flush=True)
print("outside uv: u", np.round(np.percentile(U_[o_, 0], [0, 25, 50, 75, 100]), 2).tolist(), "v", np.round(np.percentile(U_[o_, 1], [0, 25, 50, 75, 100]), 2).tolist(), flush=True)
nr_ = (r_ > 0.20) & (r_ <= 0.257)
print("near the wall inside (r 0.20-0.257):", int(nr_.sum()), "ang", np.round(np.percentile(a_[nr_], [0, 25, 50, 75, 100]), 0).tolist(), "z", np.round(np.percentile(P_[nr_, 2], [0, 50, 100]), 3).tolist(), flush=True)
print("all: z percentiles", np.round(np.percentile(P_[:, 2], [0, 10, 50, 90, 100]), 3).tolist(), "centroid rel", np.round(L_.mean(0), 3).tolist(), flush=True)
