zz_g = room_grid((zz_b,))
zz_out = []
for r_ in zz_g.rects:
    try:
        c_ = np.asarray(r_.c, float); h_ = np.asarray(r_.h, float)
    except Exception:
        c_ = np.asarray(getattr(r_, "center", [0, 0]), float); h_ = np.zeros(2)
    if -3.2 < c_[0] < -1.0 and -1.6 < c_[1] < 0.8:
        zz_out.append((getattr(r_, "name", "?"), np.round(c_, 2).tolist(), np.round(h_, 2).tolist(), round(float(getattr(r_, "yaw", 0.0)), 2), round(float(getattr(r_, "z1", -1)), 2)))
print("rect attrs", [a_ for a_ in dir(zz_g.rects[0]) if not a_.startswith("_")])
for o_ in zz_out:
    print(o_)
