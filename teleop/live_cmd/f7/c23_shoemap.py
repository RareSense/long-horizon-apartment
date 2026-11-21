zz_c = np.array([4.05, -1.74])
for zz_r in scene_rects(()):
    zz_d = float(zz_r.dist(zz_c[None])[0])
    if zz_d < 0.9:
        print(getattr(zz_r, "name", None), INFO["bodies"].get(getattr(zz_r, "name", None), {}).get("display", ""), "c", np.round(zz_r.c, 2).tolist(), "h", np.round(zz_r.h, 2).tolist(), "low", zz_r.low, "dist", round(zz_d, 2), flush=True)
for n_ in ("r105i1_shoe", "r105i2_shoe"):
    print(n_, [np.round(v_, 3).tolist() for v_ in obj_box(body_of(n_))], flush=True)
def zz_map():
    g_ = room_grid(())
    for y_ in np.arange(-0.9, -2.75, -0.1):
        print(f"{y_:5.1f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(3.0, 4.75, 0.1)), flush=True)
print("TIGHT x 3.0..4.7", flush=True); with_tight(zz_map)
print("look", bc_look(laundry_body(), "shoes_east", at=np.r_[zz_c, 0.05], dist=1.2, h=1.1, dirs=(180.0, 90.0)), flush=True)
