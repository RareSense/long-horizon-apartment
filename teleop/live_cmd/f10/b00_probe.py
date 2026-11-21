zz_b = body_of("r175i1_cardboard_box")
zz_id = m.body(zz_b).id
print("box mass", round(float(m.body_mass[zz_id]), 3), "centre", np.round(centre(zz_b), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], flush=True)
zz_g = [g_ for g_ in range(m.ngeom) if m.geom_bodyid[g_] == zz_id]
print("geoms", len(zz_g), [(int(m.geom_type[g_]), int(m.geom_contype[g_]), np.round(m.geom_size[g_], 3).tolist()) for g_ in zz_g][:12], flush=True)
for g_ in zz_g:
    if m.geom_contype[g_] and m.geom_type[g_] == 7:
        mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
        V_ = m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_]
        print(" mesh", n_, "verts; z levels", np.unique(np.round(V_[:, 2], 2)).tolist()[:20], flush=True)
# things near the box and the spot
zz_c = centre(zz_b)[:2]
for b_, inf_ in INFO["bodies"].items():
    try:
        lo_, hi_ = obj_box(b_)
    except Exception:
        continue
    cc_ = (lo_ + hi_) / 2
    if np.linalg.norm(cc_[:2] - zz_c) < 1.0 and b_ != zz_b:
        print("near", b_, np.round(cc_, 2).tolist(), "box", [np.round(v_, 2).tolist() for v_ in (lo_, hi_)], flush=True)
# static map round the box: free cells with tight clearances
g_ = with_tight(lambda: room_grid(()))
for yy_ in np.arange(1.9, 0.5, -0.1):
    print(round(float(yy_), 2), "".join("." if g_.free(np.array([xx_, yy_])) else "#" for xx_ in np.arange(-6.0, -4.2, 0.1)), flush=True)
print("x from -6.0 step 0.1; robot", state(), flush=True)
print(close(os.path.join(TELE_DIR, "box_probe.jpg"), np.r_[zz_c + np.array([0.9, -0.9]), 1.4], np.r_[zz_c, 0.1], "box"), flush=True)
