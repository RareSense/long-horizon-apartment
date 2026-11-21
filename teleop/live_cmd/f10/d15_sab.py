sb_ = body_of("r130i1_light_saber"); zid_ = m.body(sb_).id
P_ = np.vstack([m.mesh_vert[m.mesh_vertadr[m.geom_dataid[g_]]:m.mesh_vertadr[m.geom_dataid[g_]] + m.mesh_vertnum[m.geom_dataid[g_]]] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_] for g_ in range(m.ngeom) if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_] and m.geom_type[g_] == 7])
c_ = P_[:, :2].mean(0); u_ = np.linalg.svd(P_[:, :2] - c_)[2][0]; s_ = (P_[:, :2] - c_) @ u_
print("saber ends", np.round(c_ + u_ * s_.min(), 3).tolist(), np.round(c_ + u_ * s_.max(), 3).tolist(), "z", round(float(P_[:, 2].min()), 3), round(float(P_[:, 2].max()), 3), flush=True)
