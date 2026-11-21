def zz_hull(nm):
    zid_ = m.body(body_of(nm)).id; out_ = []
    for g_ in range(m.ngeom):
        if m.geom_bodyid[g_] == zid_ and m.geom_contype[g_]:
            if m.geom_type[g_] == 7:
                mid_ = m.geom_dataid[g_]; a_ = m.mesh_vertadr[mid_]; n_ = m.mesh_vertnum[mid_]
                out_.append(m.mesh_vert[a_:a_ + n_] @ d.geom_xmat[g_].reshape(3, 3).T + d.geom_xpos[g_])
            else:
                out_.append(np.array([d.geom_xpos[g_]])); print(" geom type", int(m.geom_type[g_]), np.round(m.geom_size[g_], 3).tolist())
    return out_
for nm_ in ("r139i1_toy_car", "r178i1_ball", "r179i1_toy_pouch"):
    b_ = body_of(nm_); V_ = zz_hull(nm_)
    print(nm_, "mass", round(float(m.body_mass[m.body(b_).id]), 3), "pieces", len(V_), "nverts", [len(v_) for v_ in V_], flush=True)
    for V in V_:
        if len(V) < 4: continue
        ws_ = []
        for a_ in np.radians(np.arange(0, 180, 15)):
            u_ = np.array([np.cos(a_), np.sin(a_), 0]); p_ = V @ u_; ws_.append(round(float(p_.max() - p_.min()), 3))
        print("  widths every 15 deg", ws_, "z", round(float(V[:, 2].min()), 3), round(float(V[:, 2].max()), 3), flush=True)
    try:
        gp_ = grasp_plan(b_)
        print("  grasp_plan", None if gp_ is None else {k_: (np.round(v_, 3).tolist() if isinstance(v_, np.ndarray) else v_) for k_, v_ in gp_.items() if k_ in ("point", "z", "top", "width", "wall", "score")}, flush=True)
    except Exception as ex_:
        print("  grasp_plan err", ex_, flush=True)
    print("  dest", place_for(b_), flush=True)
c_ = centre(body_of("r139i1_toy_car"))
print(close(os.path.join(TELE_DIR, "car_probe.jpg"), np.r_[c_[:2] + np.array([0.6, 0.5]), 1.2], c_, "car"), flush=True)
c_ = centre(body_of("r179i1_toy_pouch"))
print(close(os.path.join(TELE_DIR, "shelf_probe.jpg"), np.r_[c_[:2] + np.array([0.9, 0.4]), 1.3], c_, "shelf"), flush=True)
