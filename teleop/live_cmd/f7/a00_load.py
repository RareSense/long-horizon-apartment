CHAIN = r"C:\Users\raresense\sim_home\runs\1120_015326_dex1_floor_fable_blanket\checkpoints\0592_item_r117i1_blanket"
exec(open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read())
exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
print("RUN", RUN, "SEG", SEG.get("from_ckpt"), flush=True)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 6]], "done", len(DONE), DONE, flush=True)
zz_n = "r116i1_coat_pile"
zz_P = bc_w(zz_n).points(0); zz_U = bc_uv(zz_n)
print("coat n", len(zz_P), "uv ext", np.round(zz_U.min(0), 3).tolist(), np.round(zz_U.max(0), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in garment_box(zz_n)], "info", {k_: v_ for k_, v_ in GARMENTS[zz_n]["info"].items() if k_ in ("mass", "size", "kind", "file")}, flush=True)
print("hamper", np.round(bc_wall(laundry_body())[0], 3).tolist(), round(bc_wall(laundry_body())[1], 3), "rim", round(bc_rim(laundry_body()), 3), "in it", {n_: in_container(n_, laundry_body())["inside"] for n_ in GARMENTS}, flush=True)
print("kit", kit_mem(), "state", state(), flush=True)
