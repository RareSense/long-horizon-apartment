ZZ_TL = [(0.50, -0.02, 0.98), (0.53, -0.02, 1.10), (0.54, -0.02, 1.17)]
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\c09.py", encoding="utf-8").read())
P_ = zz_w().points(0); hc_ = obj_rect(zz_hb()).c; U_ = zz_uv()
out_ = np.linalg.norm(P_[:, :2] - hc_, axis=1) > 0.257
print("outside n", int(out_.sum()), "of", len(P_), "outside uv lo/hi", np.round(U_[out_].min(0), 2).tolist() if out_.any() else None, np.round(U_[out_].max(0), 2).tolist() if out_.any() else None, "outside z lo", round(float(P_[out_, 2].min()), 3) if out_.any() else None, flush=True)
