zz_log = []
for zz_mv in ZZ_MOVES:
    zz_m = thand(zz_sd, tag="bl_tele", **zz_mv)
    zz_c = contact_report()
    zz_log.append((zz_mv, zz_m["grip_pt"], round(zz_c["body"], 1), zz_c["body_who"], "fingers", zz_w.at_fingers(zz_sd), in_container("r117i1_blanket", zz_hb)["inside"], zz_m["look"]))
    if zz_m["fell"] or zz_c["body"] > 15 or zz_w.at_fingers(zz_sd) == 0:
        break
for zz_l in zz_log:
    print("MV", zz_l, flush=True)
print("blanket", in_container("r117i1_blanket", zz_hb), flush=True)
