def zz_map2(x0=-5.6, x1=-3.9, y0=1.2, y1=-1.3):
    g_ = room_grid(())
    print("      " + "".join(str(int(round(abs(x_) * 10)) % 10) for x_ in np.arange(x0, x1, 0.05)), flush=True)
    for y_ in np.arange(y0, y1, -0.05):
        print(f"{y_:5.2f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(x0, x1, 0.05)), flush=True)
print("NORMAL", flush=True); zz_map2()
print("TIGHT", flush=True); with_tight(zz_map2)
