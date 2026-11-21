M_, D_ = br.mjm, br.mjd
for g_ in range(M_.ngeom):
    if not (M_.geom_contype[g_] or M_.geom_conaffinity[g_]): continue
    if int(M_.geom_type[g_]) == 7: continue
    p_ = D_.geom_xpos[g_]; r_ = float(M_.geom_rbound[g_])
    if 0.2 < p_[0] + r_ and p_[0] - r_ < 1.2 and p_[1] - r_ < 0.0 and p_[1] + r_ > -1.0 and p_[2] - r_ < 1.2 and r_ < 3:
        print(g_, M_.body(int(M_.geom_bodyid[g_])).name[-30:], "type", int(M_.geom_type[g_]), np.round(p_, 3).tolist(), np.round(M_.geom_size[g_], 3).tolist(), flush=True)
