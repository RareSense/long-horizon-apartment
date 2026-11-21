MON["on"] = False
exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
zz_r = umbrella_to_entry()
ub_ = body_of("r107i1_umbrella")
print("UMB", {k_: v_ for k_, v_ in zz_r.items() if k_ in ("status", "why", "wall_s", "look")}, "at", np.round(centre(ub_), 3).tolist(), "kit", kit_mem(), flush=True)
print("state", state(), "fell", fallen(), "items", ck_list("item")[-2:], flush=True)
