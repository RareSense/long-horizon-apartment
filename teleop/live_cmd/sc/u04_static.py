M_, D_ = br.mjm, br.mjd
for g_ in range(M_.ngeom):
    if not (M_.geom_contype[g_] or M_.geom_conaffinity[g_]): continue
    if int(M_.geom_type[g_]) != 7: continue
    mid_ = M_.geom_dataid[g_]; a_ = M_.mesh_vertadr[mid_]; n_ = M_.mesh_vertnum[mid_]
    V_ = M_.mesh_vert[a_:a_ + n_] @ D_.geom_xmat[g_].reshape(3, 3).T + D_.geom_xpos[g_]
    lo_, hi_ = V_.min(0), V_.max(0)
    if hi_[0] > 2.6 and lo_[0] < 3.6 and hi_[1] > -2.8 and lo_[1] < -2.0 and lo_[2] < 1.2:
        print(g_, M_.body(int(M_.geom_bodyid[g_])).name[-30:], np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), flush=True)
