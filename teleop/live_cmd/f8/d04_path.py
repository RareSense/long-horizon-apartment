def zz_pp(goal):
    g_ = room_grid((zz_s,)); p_ = base()[0][:2]
    pre_ = pre_stance(g_, np.asarray(goal[:2]), goal[2])
    pth_ = g_.path(p_, np.asarray(pre_ if pre_ is not None else goal[:2]))
    print("pre", None if pre_ is None else np.round(pre_, 3).tolist(), "path", None if pth_ is None else np.round(np.asarray(pth_)[::4], 2).tolist(), flush=True)
with_tight(lambda: zz_pp((-2.295, -0.75, 0.0)))
