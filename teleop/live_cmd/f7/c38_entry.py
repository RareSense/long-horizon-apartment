zz_cb = body_of("r186i1_basket")
zz_goal = with_tight(lambda: basket_stance(zz_cb))
print("basket stance", np.round(zz_goal, 3).tolist(), flush=True)
def zz_pp():
    g_ = room_grid((zz_cb,)); p_ = base()[0][:2]
    pre_ = pre_stance(g_, zz_goal[:2], zz_goal[2])
    print("pre", None if pre_ is None else np.round(pre_, 3).tolist(), "reach cost", g_.reach_cost(p_, np.asarray(zz_goal[:2])), flush=True)
    try:
        pth_ = g_.path(p_, np.asarray(pre_ if pre_ is not None else zz_goal[:2])) if hasattr(g_, "path") else None
        print("path", None if pth_ is None else np.round(np.asarray(pth_)[::3], 2).tolist(), flush=True)
    except Exception as ex_:
        print("path err", ex_, flush=True)
zz_pp()
print("tight:", flush=True); with_tight(zz_pp)
