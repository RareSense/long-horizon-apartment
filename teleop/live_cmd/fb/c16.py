ZZ_TL = [(0.49, -0.02, 1.14)]
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\c09.py", encoding="utf-8").read())
op.run(1.0)
P_ = zz_w().points(0); U_ = zz_uv(); hc_ = obj_rect(zz_hb()).c
for uv_ in ((0.0, 0.2), (0.02, 0.24), (0.04, 0.26), (0.06, 0.28), (0.08, 0.32)):
    i_ = int(np.argmin(np.linalg.norm(U_ - np.array(uv_), axis=1)))
    L_ = P_[i_, :2] - hc_
    k_ = np.flatnonzero((np.linalg.norm(P_[:, :2] - P_[i_, :2], axis=1) < 0.02))
    print("uv", uv_, "idx", i_, "rel", np.round(L_, 3).tolist(), "r", round(float(np.linalg.norm(L_)), 3), "z", round(float(P_[i_, 2]), 3), "top z here", round(float(P_[k_, 2].max()), 3), "in_pads R", zz_in_pads("right", i_), flush=True)
