zz_b = body_of("r196i1_plastic_bag")
zz_gp = grasp_plan(zz_b)
print("gp", str(zz_gp)[:900], flush=True)
print("X_REL Y_REL", X_REL, Y_REL, "CROUCH", CROUCH, "PICK", PICK, flush=True)
def zz_bag_corners():
    zid_ = m.body(zz_b).id
    for g_ in range(m.ngeom):
        if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_]:
            mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
            V_ = m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_]
            from scipy.spatial import ConvexHull as _CH
            h_ = _CH(V_[:, :2]); P_ = V_[h_.vertices, :2]
            c_ = P_.mean(0)
            # keep the 4 points farthest from the centre (rectangle corners)
            k_ = np.argsort(-np.linalg.norm(P_ - c_, axis=1))[:4]
            C_ = P_[k_]; C_ = C_[np.argsort(np.arctan2(C_[:, 1] - c_[1], C_[:, 0] - c_[0]))]
            return C_, c_, float(V_[:, 2].min()), float(V_[:, 2].max())
zz_C, zz_c, zz_z0, zz_z1 = zz_bag_corners()
print("corners", np.round(zz_C, 3).tolist(), "centre", np.round(zz_c, 3).tolist(), "z", round(zz_z0, 4), round(zz_z1, 4), flush=True)
