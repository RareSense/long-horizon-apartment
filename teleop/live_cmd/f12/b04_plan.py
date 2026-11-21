for g_ in ((3.30, -1.15), (3.30, -1.00), (3.25, -0.80)):
    try:
        pts_ = plan_tight(g_)
        print("tight", g_, [np.round(p_, 2).tolist() for p_ in pts_], flush=True)
    except Exception as ex_:
        print("tight", g_, "ERR", str(ex_)[:200], flush=True)
    try:
        g0_ = room_grid(())
        pts_ = g0_.plan(base()[0][:2], np.asarray(g_, float))
        print("normal", g_, None if pts_ is None else [np.round(p_, 2).tolist() for p_ in pts_], flush=True)
    except Exception as ex_:
        print("normal", g_, "ERR", str(ex_)[:200], flush=True)
