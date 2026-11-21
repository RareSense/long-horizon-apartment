zz_n = "r116i1_coat_pile"
zz_P = bc_w(zz_n).points(0); zz_c = (zz_P.min(0) + zz_P.max(0)) / 2
for zz_r in scene_rects(()):
    zz_d = float(zz_r.dist(zz_c[None, :2])[0])
    if zz_d < 1.3 and getattr(zz_r, "name", None) != zz_n:
        print(getattr(zz_r, "name", None), INFO["bodies"].get(getattr(zz_r, "name", None), {}).get("display", ""), "c", np.round(zz_r.c, 2).tolist(), "h", np.round(zz_r.h, 2).tolist(), "low", zz_r.low, "top", round(float(getattr(zz_r, "top", -1)), 2), "dist", round(zz_d, 2), flush=True)
def zz_map():
    g_ = room_grid((zz_n,))
    for y_ in np.arange(-0.9, -2.85, -0.1):
        print(f"{y_:5.1f} " + "".join(("o" if (zz_P[:, :2] - [x_, y_]).__abs__().max(1).min() < 0.05 else ".") if g_.free(np.array([x_, y_])) else ("O" if (zz_P[:, :2] - [x_, y_]).__abs__().max(1).min() < 0.05 else "#") for x_ in np.arange(0.0, 2.45, 0.1)), flush=True)
print("TIGHT grid x 0.0..2.4 (o/O = coat; # blocked)", flush=True)
with_tight(zz_map)
def zz_plan():
    own_ = garment_rect(zz_n); out_ = []
    for pt in cloth_grasp_points(zz_n, k=12, sep=0.06):
        for sd in SIDES:
            g_, c_ = stance_for(pt, sd, X_REL, Y_REL, ignore=(zz_n,), with_cost=True, squat=True, clear_of=(own_,))
            if g_ is not None:
                ii_ = int(np.argmin(np.linalg.norm(zz_P[:, :2] - pt[:2], axis=1)))
                out_.append((sd, np.round(pt[:2], 2).tolist(), "uv", np.round(bc_uv(zz_n)[ii_], 2).tolist(), np.round(g_, 2).tolist(), round(float(c_), 2)))
    return out_
print("tight stances", with_tight(zz_plan), flush=True)
print("X_REL Y_REL", X_REL, Y_REL, flush=True)
