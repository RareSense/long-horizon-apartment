MON["on"] = False
print(close(os.path.join(LK, "b02_mat_above.jpg"), np.r_[1.52, -2.0, 1.6], np.r_[1.52, -2.18, 0.0], "mat from above"), flush=True)
from scipy.spatial import ConvexHull as _CH
def zz_hull(b_):
    bid_ = m.body(b_).id; P_ = []
    for g_ in range(m.ngeom):
        if m.geom_bodyid[g_] == bid_ and m.geom_contype[g_] and m.geom_type[g_] == 7:
            mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
            P_.append(m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_])
    if not P_: return None
    V_ = np.vstack(P_); h_ = _CH(V_[:, :2]); return V_[h_.vertices, :2], float(V_[:, 2].min()), float(V_[:, 2].max())
for n_ in ("r122i1_croc", "r124i1_sandal", "r124i2_sandal", "r125i1_flat", "r125i2_flat", "r105i1_shoe", "r105i2_shoe", "r107i1_umbrella", "r120i1_duck"):
    h_ = zz_hull(body_of(n_))
    print(n_, None if h_ is None else (np.round(h_[0], 3).tolist(), round(h_[1], 3), round(h_[2], 3)), flush=True)
