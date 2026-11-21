exec(open(r"E:\urc_fable4\scripts\home\live\scooter_hang.py", encoding="utf-8").read())
zz_r = park_scooter_hang("r126i1_scooter")
print("SCOOTER", {k_: v_ for k_, v_ in zz_r.items() if k_ not in ("moves",)}, flush=True)
if zz_r.get("status") == "done":
    zz_d = item_done_auto("r126i1_scooter", zz_r, spot=(-2.20, 0.0))
    print("DONE", zz_d, flush=True)
print("state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
