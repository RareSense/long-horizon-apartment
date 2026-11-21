zz_m = m.body("object_0138_body").id
print("mat body", m.body(zz_m).name, INFO["bodies"].get("object_0138_body", {}).get("display"), "xpos", np.round(d.xpos[zz_m], 3).tolist(), flush=True)
for g_ in range(m.ngeom):
    if m.geom_bodyid[g_] == zz_m:
        print(" geom", m.geom(g_).name, int(m.geom_type[g_]), np.round(d.geom_xpos[g_], 3).tolist(), np.round(m.geom_size[g_], 3).tolist(), np.round(d.geom_xmat[g_].reshape(3, 3)[:, 0], 2).tolist(), flush=True)
zz_c = body_of("r122i1_croc")
print("croc", np.round(centre(zz_c), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(zz_c)], "z axis", np.round(d.xmat[m.body(zz_c).id].reshape(3, 3)[:, 2], 2).tolist(), flush=True)
print("place_for croc", place_for(zz_c), "spot", (DESC.get("spots") or {}).get("r122i1_croc"), (DESC.get("spots") or {}).get("r105i1_shoe"), (DESC.get("spots") or {}).get("r105i2_shoe"), (DESC.get("spots") or {}).get("r124i1_sandal"), flush=True)
