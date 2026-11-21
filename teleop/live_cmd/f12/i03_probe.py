zz_b = body_of("r149i1_pouch")
lo_, hi_ = obj_box(zz_b)
print("pouch box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "mass", round(float(m.body_mass[m.body(zz_b).id]), 3), flush=True)
gp_ = grasp_plan(zz_b)
print("grasp_plan", {k_: (np.round(v_, 3).tolist() if hasattr(v_, "tolist") else v_) for k_, v_ in (gp_ or {}).items() if k_ in ("point", "z", "top", "closes", "width", "how", "section")}, flush=True)
C_ = flat_corners(zz_b)
print("hull corners", np.round(C_[0], 3).tolist(), "c", np.round(C_[1], 3).tolist(), "z", round(C_[2], 3), round(C_[3], 3), flush=True)
from scipy.spatial import ConvexHull as _CH3
zid_ = m.body(zz_b).id
for g_ in range(m.ngeom):
    if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_]:
        mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
        V_ = m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_]
        h_ = _CH3(V_[:, :2])
        print("geom", g_, "nv", n_, "hull2d", np.round(V_[h_.vertices, :2], 3).tolist(), flush=True)
print("state", state(), "bin", np.round(centre(body_of("rubbish_bin")), 3).tolist(), flush=True)
