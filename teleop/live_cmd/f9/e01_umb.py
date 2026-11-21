zz_u = body_of("r106i1_umbrella"); zid_ = m.body(zz_u).id
print("mass", round(float(m.body_mass[zid_]), 3), "com", np.round(d.xipos[zid_], 3).tolist(), flush=True)
P_ = piece_points(zz_u)
print("pieces", len(P_), flush=True)
for k_, V_ in list(P_.items())[:30]:
    print(" ", k_, "n", len(V_), "min", np.round(V_.min(0), 3).tolist(), "max", np.round(V_.max(0), 3).tolist(), flush=True)
gp_ = grasp_plan(zz_u)
print("grasp_plan", str(gp_)[:500], flush=True)
def zz_m(x0=1.4, x1=3.8, y0=0.2, y1=-2.0, st=0.1):
    g_ = room_grid((zz_u,))
    print("      " + "".join(str(int(round(abs(x_) * 10)) % 10) for x_ in np.arange(x0, x1, st)), flush=True)
    for y_ in np.arange(y0, y1, -st):
        print(f"{y_:5.2f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(x0, x1, st)), flush=True)
print("TIGHT umbrella left out", flush=True); with_tight(zz_m)
