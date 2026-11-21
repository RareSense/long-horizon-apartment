zz_n = "r117i1_blanket"
P_ = bc_w(zz_n).points(0); pt_ = P_[136]
def _diag():
    g = room_grid((zz_n,))
    p, yaw0 = base()
    for k in range(12):
        yw = wrapa(k * np.pi / 6)
        b = pt_[:2] - RM.rz(yw)[:2, :2] @ np.array([X_REL, -Y_REL])
        dist = g.reach_cost(p[:2], b)
        kc = knees_clear(g, b, yw) if np.isfinite(dist) else None
        fc = feet_clear(b, yw, [r for r in g.rects if r.low]) if np.isfinite(dist) else None
        print("yaw", k * 30, "b", np.round(b, 2).tolist(), "dist", round(float(dist), 2), "knees", kc, "feet", fc, flush=True)
    for q_pt in ((0.5, -1.0), (0.0, -1.0), (-1.0, -1.0), (0.9, -1.5), (0.3, -0.3)):
        print("reach", q_pt, round(float(g.reach_cost(p[:2], np.array(q_pt))), 2), flush=True)
with_tight(_diag)
for b_ in INFO["bodies"]:
    try:
        c_ = centre(b_)
    except Exception:
        continue
    if 0.3 < c_[0] < 1.6 and -2.4 < c_[1] < -0.9:
        print("thing", b_, INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist(), flush=True)
