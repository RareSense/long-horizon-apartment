print("hat", in_container("r131i1_knit_hat", zz_hb), flush=True)
zz_log = []
for zz_mv in [dict(dz=0.04), dict(dz=0.04), dict(dx=-0.04), dict(dx=-0.04), dict(dx=-0.04), dict(dx=-0.04)]:
    zz_m = thand("left", tag="hat_out", **zz_mv)
    zz_c = contact_report()
    zz_log.append((zz_mv, zz_m["grip_pt"], zz_c["body"], zz_c["body_who"], zz_m["look"]))
    if zz_c["body"] > 15 or zz_m["fell"]:
        break
for zz_l in zz_log:
    print("MV", zz_l)
print("hat", in_container("r131i1_knit_hat", zz_hb), flush=True)
