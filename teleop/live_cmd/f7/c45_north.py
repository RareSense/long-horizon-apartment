ck_load(os.path.join(RUN, "checkpoints", "1050_act_walk_leg")); gait_on(); settle_after_load()
zz_cb = body_of("r186i1_basket")
print("loaded", state(), "basket", np.round(centre(zz_cb), 3).tolist(), "held", list(HELD), "BASKET_HELD", list(BASKET_HELD), flush=True)
mon_start(target=None); MON["t_max"] = 900.0; MON["trace"] = []
MON["ignore_names"] = (zz_cb,)
zz_o = []
try:
    for zz_g in ((-1.20, -0.38, np.pi), (-1.75, -0.38, np.pi), (-2.25, -0.40, np.pi)):
        w_ = walk_tight(zz_g, carry=SIDES)
        zz_o.append((zz_g[:2], w_.get("err_xy") if isinstance(w_, dict) else w_))
        print("leg", zz_g[:2], zz_o[-1][1], state()["pelvis"], "touch", contact_report()["body"], "basket", np.round(centre(zz_cb), 3).tolist(), flush=True)
except Abort as ex_:
    zz_o.append(("abort", str(ex_)))
except RuntimeError as ex_:
    zz_o.append(("error", str(ex_)[:200]))
MON["on"] = False
print("OUT", zz_o, "state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
print("look", look3("basket_north_route"), flush=True)
