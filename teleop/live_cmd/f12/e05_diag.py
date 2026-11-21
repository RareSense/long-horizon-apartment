cc_ = umb_contacts()
print("contacts", cc_, flush=True)
print("normal sum world", round(sum(c_[3] for c_ in cc_ if c_[0] in ("world", "scene_static")), 2), "weight", round(float(m.body_mass[m.body(UMB).id]) * 9.81, 2), flush=True)
M_ = br.mjm; zid_ = br_body_id(UMB)
for g_ in range(M_.ngeom):
    if M_.geom_bodyid[g_] == zid_:
        print("geom", g_, "type", int(M_.geom_type[g_]), "contype", int(M_.geom_contype[g_]), "conaff", int(M_.geom_conaffinity[g_]), "friction", M_.geom_friction[g_].tolist(), "condim", int(M_.geom_condim[g_]), "mass body", float(M_.body_mass[zid_]), flush=True)
print("ee gains?", {k_: v_ for k_, v_ in (getattr(ts.ctrl, "g", {}) or {}).items() if "ee" in str(k_).lower() or "arm" in str(k_).lower()} if hasattr(ts.ctrl, "g") else None, flush=True)
