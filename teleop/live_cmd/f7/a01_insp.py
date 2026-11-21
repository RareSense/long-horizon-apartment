zz_n = "r116i1_coat_pile"
zz_P = bc_w(zz_n).points(0); zz_U = bc_uv(zz_n)
def zz_plan():
    own_ = garment_rect(zz_n); out_ = []
    for pt in cloth_grasp_points(zz_n, k=12, sep=0.06):
        nr = np.linalg.norm(zz_P[:, :2] - pt[:2], axis=1) < 0.03
        rel_ = float(np.ptp(zz_P[nr, 2])) if nr.any() else 0
        ii_ = int(np.argmin(np.linalg.norm(zz_P[:, :2] - pt[:2], axis=1) + 0.0 * zz_P[:, 2]))
        g_, c_ = stance_for(pt, "right", X_REL, Y_REL, ignore=(zz_n,), with_cost=True, squat=True, clear_of=(own_,))
        out_.append((np.round(pt[:2], 2).tolist(), "relief", round(rel_, 3), "uv", np.round(zz_U[ii_], 2).tolist(), "stance", None if g_ is None else np.round(g_, 2).tolist(), round(float(c_), 2) if g_ is not None else None))
    return out_
print("NORMAL", flush=True)
for r_ in zz_plan(): print(r_, flush=True)
print("TIGHT", flush=True)
for r_ in with_tight(zz_plan): print(r_, flush=True)
zz_c = (zz_P.min(0) + zz_P.max(0)) / 2
print("look", zz_look_dummy if False else bc_look(laundry_body(), "coat_lying", at=np.r_[zz_c[:2], 0.05], dist=1.4, h=1.2, dirs=(90.0, 270.0)), flush=True)
