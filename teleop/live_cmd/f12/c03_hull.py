zid_ = m.body(UMB).id
for g_ in range(m.ngeom):
    if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_]:
        mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
        V_ = m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_]
        print("geom", g_, "nvert", n_, "friction", m.geom_friction[g_].tolist(), "margin", float(m.geom_margin[g_]), flush=True)
        # east part: vertices with x > 2.6, sorted by y, with z
        E_ = V_[V_[:, 0] > 2.55]
        for v_ in E_[np.argsort(E_[:, 1])]:
            print("  v", np.round(v_, 3).tolist(), flush=True)
P_, Eq_ = slab_hull()
print("hull2d", np.round(P_, 3).tolist(), flush=True)
print("pads now", np.round(pad_mid("left"), 3).tolist(), "fingertip z", flush=True)
