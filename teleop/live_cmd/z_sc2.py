for r_ in zz_g.rects:
    c_ = np.asarray(r_.c, float)
    if -2.6 < c_[0] < -0.6 and 0.0 < c_[1] < 2.5:
        print("N", r_.name, np.round(c_, 2).tolist(), np.round(np.asarray(r_.h), 2).tolist(), round(float(r_.yaw), 2))
print("grid lo hi", np.round(zz_g.lo, 2), np.round(zz_g.hi, 2))
for zz_y in np.arange(1.2, -1.3, -0.1):
    print(round(float(zz_y), 2), "".join("#" if not zz_g.free(np.array([zz_x, zz_y]), -0.20) else "." for zz_x in np.arange(-3.0, -0.6, 0.05)))
zz_sab = body_of("r130i1_light_saber")
print("saber", zz_sab, "dest", DESC["destinations"].get("r130i1_light_saber"), DESC["spots"].get("r130i1_light_saber"), [np.round(v_, 3).tolist() for v_ in obj_box(zz_sab)], "mass", float(m.body_mass[m.body(zz_sab).id]))
print("route has saber at", [i_ for i_, s_ in enumerate(ROUTE) if item_name(s_) == "r130i1_light_saber"], "scooters", [(i_, item_name(s_)) for i_, s_ in enumerate(ROUTE) if "scooter" in str(item_name(s_))])
print("r126 step", [s_ for s_ in ROUTE if item_name(s_) == "r126i1_scooter"])
