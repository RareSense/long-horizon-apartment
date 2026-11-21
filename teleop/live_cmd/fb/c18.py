P_ = zz_w().points(0); U_ = zz_uv()
pm_ = pad_mid("right"); a_, b_ = pads("right")
for nm_, q_xy in (("mid", pm_), ("padA", a_), ("padB", b_)):
    k_ = np.flatnonzero(np.linalg.norm(P_[:, :2] - q_xy[:2], axis=1) < 0.015)
    if len(k_):
        i_ = k_[np.argmax(P_[k_, 2])]
        print(nm_, "xy", np.round(q_xy[:2], 3).tolist(), "top particle", int(i_), "z", round(float(P_[i_, 2]), 3), "uv", np.round(U_[i_], 2).tolist(), "n", len(k_), "zs", np.round(np.sort(P_[k_, 2])[-5:], 3).tolist(), flush=True)
    else:
        print(nm_, "xy", np.round(q_xy[:2], 3).tolist(), "no cloth below", flush=True)
# profile along the closing axis through the pad middle (east-west), 1 cm steps: top z
ax_ = (b_ - a_); ax_[2] = 0; ax_ /= np.linalg.norm(ax_)
row_ = []
for s_ in np.arange(-0.07, 0.071, 0.01):
    q_xy = pm_[:2] + ax_[:2] * s_
    k_ = np.flatnonzero(np.linalg.norm(P_[:, :2] - q_xy, axis=1) < 0.008)
    row_.append(f"{s_:+.2f}:{(P_[k_, 2].max() if len(k_) else float('nan')):.3f}")
print("top z along the closing axis (pad A at -, pad B at +):", " ".join(row_), "pad_low", round(pad_low("right"), 3), "half gap", round(float(np.linalg.norm(b_ - a_)) / 2, 3), flush=True)
