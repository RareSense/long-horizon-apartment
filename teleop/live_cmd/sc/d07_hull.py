MON["on"] = False
LD = "0005_act_walk_path"; exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\sc\ld.py", encoding="utf-8").read())
b_ = body_of("r120i1_duck"); bid_ = m.body(b_).id
P_ = []
for g_ in range(m.ngeom):
    if m.geom_bodyid[g_] == bid_ and m.geom_contype[g_]:
        mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
        P_.append(m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_])
        print("geom", g_, "type", m.geom_type[g_], "nv", n_, flush=True)
V_ = np.vstack(P_)
for z0_, z1_ in ((0.0, 0.02), (0.02, 0.04), (0.04, 0.055), (0.055, 0.07), (0.07, 0.085)):
    S_ = V_[(V_[:, 2] >= z0_) & (V_[:, 2] < z1_)]
    if len(S_): print("z", z0_, z1_, "x", np.round([S_[:, 0].min(), S_[:, 0].max()], 3).tolist(), "y", np.round([S_[:, 1].min(), S_[:, 1].max()], 3).tolist(), "n", len(S_), flush=True)
print("JAW", {k_: globals().get(k_) for k_ in ("JAW_OPEN", "JAW_MAX", "OPEN_GAP")}, flush=True)
