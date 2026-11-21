# List what is left on the route: name, kind, where, height, destination, nearest other thing (for easiest-first order)
zz_rows = []
for zz_i, zz_s in enumerate(ROUTE[POS:]):
    zz_nm = item_name(zz_s)
    zz_b = body_of(zz_nm) if isinstance(zz_nm, str) else None
    if zz_b in INFO["bodies"]:
        zz_lo, zz_hi = obj_box(zz_b); zz_c = (zz_lo + zz_hi) / 2
        zz_nn = sorted((float(np.linalg.norm(((obj_box(b2)[0] + obj_box(b2)[1]) / 2)[:2] - zz_c[:2])), INFO["bodies"][b2].get("display", b2)) for b2 in INFO["bodies"] if b2 != zz_b)[:2]
        zz_rows.append((zz_i, zz_s[0], zz_nm, np.round(zz_c[:2], 2).tolist(), round(float(zz_lo[2]), 2), round(float(zz_hi[2] - zz_lo[2]), 2), DESC["destinations"].get(zz_nm), [(round(a, 2), b) for a, b in zz_nn]))
    else:
        zz_rows.append((zz_i, zz_s[0], zz_nm, None, None, None, DESC["destinations"].get(zz_nm) if isinstance(zz_nm, str) else None, None))
for zz_r in zz_rows:
    print("IT", zz_r)
print("POS", POS, "len", len(ROUTE), "DONE", len(DONE), flush=True)
