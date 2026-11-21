exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
zz_n = "r116i1_coat_pile"
print("held", cloth_held("right"), "hang", round(float(pad_mid("right")[2] - garment_box(zz_n)[0][2]), 3), "held uv", np.round(bc_uv(zz_n)[LOCK["right"][1]].mean(0), 3).tolist(), flush=True)
BC["stage"] = "grasp"
print("ck", ck_save("bc_coat_held_right", kind="act"), flush=True)
MON["trace"] = []
zz_r = bigcloth_into(zz_n, s1="right", start="carry", stop_after="carry")
print("RESULT", zz_r, flush=True)
print("trace", MON["trace"][::4], flush=True)
print("state", state(), "touch", contact_report(), "kit", kit_mem(), "lowest", round(float(bc_w(zz_n).points(0)[:, 2].min()), 3), flush=True)
print("look3", look3("coat_at_pre"), flush=True)
