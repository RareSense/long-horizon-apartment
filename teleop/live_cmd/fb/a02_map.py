zz_c = obj_rect(zz_hb()).c
for zz_r in scene_rects(()):
    zz_d = float(zz_r.dist(zz_c[None])[0])
    if zz_d < 1.3:
        print(getattr(zz_r, "name", None), "c", np.round(zz_r.c, 2).tolist(), "h", np.round(zz_r.h, 2).tolist(), "yaw", round(float(getattr(zz_r, "yaw", 0.0)), 2), "low", zz_r.low, "top", round(float(getattr(zz_r, "top", -1)), 2), "dist", round(zz_d, 2), flush=True)
print("look", zz_look(np.r_[zz_c, 0.4], "hamper_now", dist=1.7, h=1.6, dirs=(90.0, 0.0), top=True), flush=True)
