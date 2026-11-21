zz_b = body_of("r196i1_plastic_bag"); zz_id = m.body(zz_b).id
print("body pos", np.round(d.xpos[zz_id], 3).tolist(), "R z", np.round(d.xmat[zz_id].reshape(3, 3)[:, 2], 3).tolist(), flush=True)
for g_ in range(m.ngeom):
    if m.geom_bodyid[g_] != zz_id: continue
    t_ = int(m.geom_type[g_]); print("geom", g_, "type", t_, "size", np.round(m.geom_size[g_], 4).tolist(), "contype", int(m.geom_contype[g_]), "conaff", int(m.geom_conaffinity[g_]), "pos", np.round(d.geom_xpos[g_], 3).tolist(), flush=True)
    if t_ == 7:
        mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
        V_ = m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_]
        print(" nvert", n_, "min", np.round(V_.min(0), 3).tolist(), "max", np.round(V_.max(0), 3).tolist(), flush=True)
        # width along y (world) at x slices
        for x_ in np.arange(V_[:, 0].min(), V_[:, 0].max() + 1e-6, 0.03):
            s_ = V_[np.abs(V_[:, 0] - x_) < 0.02]
            if len(s_): print("  x %.3f y %.3f..%.3f z %.3f..%.3f" % (x_, s_[:, 1].min(), s_[:, 1].max(), s_[:, 2].min(), s_[:, 2].max()), flush=True)
        print(" verts xy", np.round(V_[:, :2], 3).tolist()[:60], flush=True)
