print(floor_first(["r68i1_rag"]), flush=True)
print("rag box", [np.round(v_, 3).tolist() for v_ in garment_box("r68i1_rag")], "pile top in hamper", round(max(float(bc_w(n_).points(0)[:, 2].max()) for n_ in ("r116i1_coat_pile", "r117i1_blanket")), 3), flush=True)
MON["trace"] = []
zz_r = go_item()
print("ITEM", zz_r, flush=True)
print("state", state(), "rag", in_container("r68i1_rag", laundry_body()), "coat", in_container("r116i1_coat_pile", laundry_body()), "kit", kit_mem(), flush=True)
