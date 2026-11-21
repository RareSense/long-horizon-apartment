def zz_map4(x0=-2.6, x1=2.0, y0=0.2, y1=-2.65, st=0.1):
    g_ = room_grid((zz_s,))
    print("      " + "".join(str(int(round(abs(x_) * 10)) % 10) for x_ in np.arange(x0, x1, st)), flush=True)
    for y_ in np.arange(y0, y1, -st):
        print(f"{y_:5.2f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(x0, x1, st)), flush=True)
print("TIGHT, scooter left out, x -2.6..2.0 step 0.1", flush=True); with_tight(zz_map4)
print("slipper", np.round(centre(body_of("r123i1_slipper")), 2).tolist(), "bike", [ (INFO["bodies"][b_].get("display"), np.round(centre(b_),2).tolist()) for b_ in INFO["bodies"] if "bike" in str(INFO["bodies"][b_].get("display")) or "r127" in str(INFO["bodies"][b_].get("display"))], flush=True)
