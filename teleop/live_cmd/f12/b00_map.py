ub_ = body_of("r106i1_umbrella")
for n_ in ("r105i1_shoe", "r105i2_shoe", "r102i1_tote", "r101i1_stroller", "r120i1_duck", "r107i1_umbrella", "r108i1_scissors"):
    try:
        b_ = body_of(n_)
        print(n_, b_, "dest", DESC["destinations"].get(n_), (DESC.get("spots") or {}).get(n_), "at", np.round(centre(b_), 3).tolist(), "box", [np.round(v_, 2).tolist() for v_ in obj_box(b_)], "mass", round(float(m.body_mass[m.body(b_).id]), 2), "dyn", INFO["bodies"].get(b_, {}).get("dynamic"), flush=True)
    except Exception as ex_:
        print(n_, "ERR", str(ex_)[:120], flush=True)
g_ = with_tight(lambda: room_grid((ub_,)), rb0=0.22, rf0=0.12)
print("grid rb0 0.22 ignoring the umbrella; columns x from 0.0 step 0.1 to 3.9")
for yy_ in np.arange(1.0, -2.75, -0.1):
    print(f"{yy_:6.2f}", "".join("." if g_.free(np.array([xx_, yy_])) else "#" for xx_ in np.arange(0.0, 3.91, 0.1)), flush=True)
print(close(os.path.join(TELE_DIR, "f12_hall_top.jpg"), np.array([2.0, -0.7, 3.2]), np.array([2.0, -1.3, 0.0]), "hall top"), flush=True)
print(close(os.path.join(TELE_DIR, "f12_hall_side.jpg"), np.array([0.6, -0.3, 1.6]), np.array([2.3, -1.3, 0.0]), "hall side"), flush=True)
