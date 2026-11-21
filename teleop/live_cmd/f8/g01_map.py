zz_s = body_of("r126i1_scooter")
def zz_map3(x0=-3.0, x1=-0.5, y0=1.0, y1=-1.9):
    g_ = room_grid((zz_s,))
    print("      " + "".join(str(int(round(abs(x_) * 10)) % 10) for x_ in np.arange(x0, x1, 0.05)), flush=True)
    for y_ in np.arange(y0, y1, -0.05):
        print(f"{y_:5.2f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(x0, x1, 0.05)), flush=True)
print("TIGHT, scooter left out", flush=True); with_tight(zz_map3)
for n_ in ("r132i1_heater", "r133i1_laundry_basket"):
    b_ = body_of(n_)
    if b_ in INFO["bodies"]: print(n_, [np.round(v_, 2).tolist() for v_ in obj_box(b_)], flush=True)
print("statics near", [(r_[0] if isinstance(r_, (tuple, list)) else r_) for r_ in []], flush=True)
