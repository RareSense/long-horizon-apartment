exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
b_ = body_of("r100i1_towel"); bid_ = m.body(b_).id
print("towel", b_, "kg", round(float(m.body_mass[bid_]), 3), "geoms", [(g_, int(m.geom_type[g_]), int(m.geom_contype[g_])) for g_ in range(m.ngeom) if m.geom_bodyid[g_] == bid_][:8], flush=True)
V_ = _hull_pts(b_)
for z0_ in np.arange(0.2, 0.65, 0.05):
    S_ = V_[(V_[:, 2] >= z0_) & (V_[:, 2] < z0_ + 0.05)]
    if len(S_): print("z", round(z0_, 2), "x", np.round([S_[:, 0].min(), S_[:, 0].max()], 3).tolist(), "y", np.round([S_[:, 1].min(), S_[:, 1].max()], 3).tolist(), "n", len(S_), flush=True)
print("info", {k_: v_ for k_, v_ in INFO["bodies"][b_].items() if k_ in ("display", "cls", "category", "grips", "lbox")}, flush=True)
# what is under / around it (static)
M_, D_ = br.mjm, br.mjd
for g_ in range(M_.ngeom):
    if not (M_.geom_contype[g_] or M_.geom_conaffinity[g_]) or int(M_.geom_type[g_]) != 7: continue
    mid_ = M_.geom_dataid[g_]; a_ = M_.mesh_vertadr[mid_]; n_ = M_.mesh_vertnum[mid_]
    W_ = M_.mesh_vert[a_:a_ + n_] @ D_.geom_xmat[g_].reshape(3, 3).T + D_.geom_xpos[g_]
    lo_, hi_ = W_.min(0), W_.max(0)
    if hi_[0] > -1.4 and lo_[0] < -0.4 and hi_[1] > 0.9 and lo_[1] < 2.0 and "Dex1" not in M_.body(int(M_.geom_bodyid[g_])).name and "_link" not in M_.body(int(M_.geom_bodyid[g_])).name:
        print("near", g_, M_.body(int(M_.geom_bodyid[g_])).name[-28:], np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), flush=True)
c_ = centre(b_)
print(close(os.path.join(LK, "t01_towel_a.jpg"), np.r_[c_[0] + 0.3, c_[1] - 1.1, 1.2], c_, "towel from south"), flush=True)
print(close(os.path.join(LK, "t01_towel_b.jpg"), np.r_[c_[0] - 0.9, c_[1] - 0.6, 1.0], c_, "towel from SW"), flush=True)
