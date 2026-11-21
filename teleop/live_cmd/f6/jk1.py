# AI teleop (AI-operated): free the right gripper from the hamper wall after the jacket drop, step away, rest
zz_log = []
for zz_mv in [dict(dz=0.04), dict(dz=0.04), dict(dy=0.04), dict(dy=0.04), dict(dy=0.04), dict(dy=0.04)]:
    zz_m = thand("right", tag="jk_out", **zz_mv)
    zz_c = contact_report()
    zz_log.append((zz_mv, zz_m["grip_pt"], zz_c["body"], zz_c["body_who"], zz_m["look"]))
    if zz_m["fell"] or (zz_c["body"] > 35):
        break
for zz_l in zz_log:
    print("MV", zz_l, flush=True)
print("jacket", in_container("r121i1_jacket", zz_hb), state(), flush=True)
