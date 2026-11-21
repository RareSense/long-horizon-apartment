tgt_ = np.array([0.91, -1.5])
def _diag2():
    g = room_grid(("r117i1_blanket",))
    p, yaw0 = base()
    out_ = []
    for dx in np.arange(-0.4, 0.61, 0.1):
        for dy in np.arange(-0.4, 0.61, 0.1):
            s_ = p[:2] + np.array([dx, dy])
            c_ = g.reach_cost(s_, tgt_)
            if np.isfinite(c_):
                out_.append((round(float(np.hypot(dx, dy)), 2), np.round(s_, 2).tolist(), round(float(c_), 2)))
    out_.sort()
    print("free starts near the robot (dist, start, cost to 0.91,-1.5):", out_[:10], flush=True)
print("TIGHT"); with_tight(_diag2)
print("NORMAL"); _GRID.clear(); _diag2()
