print("state", state(), "near", near_things(0.8), flush=True)
def _d():
    g = room_grid(())
    print("cost to (0.0,-1.9)", round(float(g.reach_cost(base()[0][:2], np.array([0.0, -1.9]))), 2), flush=True)
_d(); _GRID.clear(); with_tight(_d)
