MON["on"] = False
M_, D_ = br.mjm, br.mjd
for g_ in range(M_.ngeom):
    if not (M_.geom_contype[g_] or M_.geom_conaffinity[g_]): continue
    p_ = D_.geom_xpos[g_]
    if not (1.0 < p_[0] < 2.1 and -2.7 < p_[1] < -1.8): continue
    nm_ = M_.body(int(M_.geom_bodyid[g_])).name[-40:]
    if int(M_.geom_type[g_]) == 7:
        mid_ = M_.geom_dataid[g_]; a_ = M_.mesh_vertadr[mid_]; n_ = M_.mesh_vertnum[mid_]
        V_ = M_.mesh_vert[a_:a_ + n_] @ D_.geom_xmat[g_].reshape(3, 3).T + p_
        lo_ = V_[V_[:, 2] < 0.15]
        print(g_, nm_, "aabb", np.round(V_.min(0), 3).tolist(), np.round(V_.max(0), 3).tolist(), "below 0.15:", (np.round(lo_.min(0), 3).tolist(), np.round(lo_.max(0), 3).tolist()) if len(lo_) else None, flush=True)
    else:
        print(g_, nm_, "type", int(M_.geom_type[g_]), np.round(p_, 3).tolist(), np.round(M_.geom_size[g_], 3).tolist(), flush=True)
