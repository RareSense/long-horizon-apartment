zz_P = zz_w().points(0)
zz_c = zz_P[994][:2]
for zz_r in scene_rects(()):
    zz_d = float(zz_r.dist(zz_c[None])[0])
    if zz_d < 1.5:
        print(getattr(zz_r, "name", None), "c", np.round(zz_r.c, 2).tolist(), "h", np.round(zz_r.h, 2).tolist(), "yaw", round(float(getattr(zz_r, "yaw", 0.0)), 2), "low", zz_r.low, "top", round(float(getattr(zz_r, "top", -1)), 2), "dist", round(zz_d, 2), flush=True)
g_ = room_grid((zz_BL,))
# free map around the blanket: rows y from -0.6 down to -2.6, cols x from 0.4 to 2.8, 0.1 m cells
for y_ in np.arange(-0.6, -2.65, -0.1):
    print(f"{y_:5.1f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(0.4, 2.85, 0.1)), flush=True)
print("x: 0.4 .. 2.8 step 0.1; blanket x 1.13..2.02 y -2.02..-1.26", flush=True)
