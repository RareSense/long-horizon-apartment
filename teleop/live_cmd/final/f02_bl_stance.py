zz_n = "r117i1_blanket"
P_ = bc_w(zz_n).points(0)
ip_ = bc_particle(zz_n, (-0.43, 0.0))
print("uv particle", ip_, np.round(P_[ip_], 3).tolist(), "p136", np.round(P_[136], 3).tolist(), "garment box", [np.round(v_, 3).tolist() for v_ in garment_box(zz_n)], flush=True)
for lab_, kw_ in (("fable", dict(ignore=(zz_n,), squat=True, clear_of=(garment_rect(zz_n),))), ("skill", dict(ignore=(zz_n,), squat=True, clear_of=()))):
    for ipx_ in (136, ip_):
        try:
            g_ = with_tight(lambda: stance_for(np.r_[P_[ipx_][:2], 0.0], "right", X_REL, Y_REL, **kw_))
            print(lab_, ipx_, "goal", None if g_ is None else np.round(g_, 3).tolist(), flush=True)
        except Exception as ex_:
            print(lab_, ipx_, "ERR", str(ex_)[:160], flush=True)
print("near (0.91,-1.5):", [(b_, INFO["bodies"][b_].get("display"), np.round(centre(b_)[:2], 2).tolist()) for b_ in INFO["bodies"] if INFO["bodies"][b_].get("free", True) and np.linalg.norm(centre(b_)[:2] - np.array([0.91, -1.5])) < 0.7] if True else None, flush=True)
