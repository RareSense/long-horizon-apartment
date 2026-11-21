MON["on"] = False
ck_save("before_scout_duck", kind="start")
exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
zz_r = duck_to_basket()
print("DUCK", {k_: v_ for k_, v_ in zz_r.items() if k_ in ("status", "why", "wall_s", "look")}, flush=True)
print("state", state(), "fell", fallen(), "in", inside(body_of("r120i1_duck"), body_of("r186i1_basket")), "route next", [item_name(s_) for s_ in ROUTE[POS:POS + 3]], flush=True)
