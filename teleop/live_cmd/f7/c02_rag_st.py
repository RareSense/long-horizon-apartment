zz_n = "r68i1_rag"; zz_P = bc_w(zz_n).points(0); zz_U = bc_uv(zz_n)
print("rag uv ext", np.round(zz_U.min(0), 3).tolist(), np.round(zz_U.max(0), 3).tolist(), "n", len(zz_P), flush=True)
zz_c = (zz_P.min(0) + zz_P.max(0)) / 2
for zz_r in scene_rects(()):
    zz_d = float(zz_r.dist(zz_c[None, :2])[0])
    if zz_d < 0.8 and getattr(zz_r, "name", None) != zz_n:
        print(getattr(zz_r, "name", None), INFO["bodies"].get(getattr(zz_r, "name", None), {}).get("display", ""), "c", np.round(zz_r.c, 2).tolist(), "h", np.round(zz_r.h, 2).tolist(), "low", zz_r.low, "dist", round(zz_d, 2), flush=True)
def zz_try():
    out_ = []
    for uv_ in ((0.10, 0.0), (-0.10, 0.0), (0.0, 0.08), (0.0, -0.08), (0.10, 0.08), (-0.10, -0.08), (0.10, -0.08), (-0.10, 0.08)):
        ip_ = bc_particle(zz_n, uv_); pt = np.r_[zz_P[ip_][:2], 0.0]
        for sd in SIDES:
            g_, c_ = stance_for(pt, sd, X_REL, Y_REL, ignore=(zz_n,), with_cost=True, squat=True)
            if g_ is not None:
                out_.append((uv_, sd, np.round(pt[:2], 2).tolist(), np.round(g_, 2).tolist(), round(float(c_), 2)))
    return out_
print("normal", zz_try(), flush=True)
print("tight", with_tight(zz_try), flush=True)
print("look", bc_look(laundry_body(), "rag_lying", at=np.r_[zz_c[:2], 0.05], dist=1.2, h=1.0, dirs=(0.0, 90.0, 180.0)), flush=True)
