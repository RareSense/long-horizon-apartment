def zz_map():
    g_ = room_grid(())
    p_ = base()[0][:2]
    print("reach cost to (3.9,-2.1):", g_.reach_cost(p_, np.array([3.9, -2.1])), "to (2.5,-1.5)", g_.reach_cost(p_, np.array([2.5, -1.5])), flush=True)
    for y_ in np.arange(1.6, -2.75, -0.1):
        print(f"{y_:5.1f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(0.8, 4.6, 0.1)), flush=True)
print("TIGHT x 0.8..4.5", flush=True); with_tight(zz_map)
