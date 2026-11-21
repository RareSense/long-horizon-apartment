pb_ = body_of("r179i1_toy_pouch"); zid_ = m.body(pb_).id
for g_ in range(m.ngeom):
    if m.geom_bodyid[g_] == zid_:
        print("geom", g_, int(m.geom_type[g_]), "contype", int(m.geom_contype[g_]), "conaff", int(m.geom_conaffinity[g_]), m.geom(g_).name, flush=True)
P_ = np.vstack([m.mesh_vert[m.mesh_vertadr[m.geom_dataid[g_]]:m.mesh_vertadr[m.geom_dataid[g_]] + m.mesh_vertnum[m.geom_dataid[g_]]] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_] for g_ in range(m.ngeom) if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_] and m.geom_type[g_] == 7])
z0_, z1_ = P_[:, 2].min(), P_[:, 2].max()
for zz_ in np.linspace(z0_ + 0.01, z1_ - 0.003, 10):
    S_ = P_[np.abs(P_[:, 2] - zz_) < 0.006]
    if len(S_) < 3: continue
    print(round(float(zz_), 3), "n", len(S_), "x", round(float(np.ptp(S_[:, 0])), 3), "y", round(float(np.ptp(S_[:, 1])), 3), flush=True)
print("mass", float(m.body_mass[zid_]), "friction", np.round(m.geom_friction[[g_ for g_ in range(m.ngeom) if m.geom_bodyid[g_] == zid_][0]], 2).tolist(), flush=True)
