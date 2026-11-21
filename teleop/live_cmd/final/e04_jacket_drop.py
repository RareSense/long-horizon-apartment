# jacket: go_item held it but hit the 240 s item cap before the drop (standing by the hamper, right hand holding).
# Finish: drop_in_cloth from here under the monitor (cap 400 s). AI-operated
nm_ = "r121i1_jacket"; hb_ = "r133i1_laundry_basket"
print("start", state(), "LOCK", list(LOCK), "at fingers", GARMENTS[nm_]["w"].at_fingers("right"), flush=True)
mon_start(target=None); MON["t_max"] = 400.0
MON["last_touch"]["right"] = float(d.time)
o_ = {}
try:
    o_ = drop_in_cloth(nm_, hb_, "right")
except Abort as ex_:
    o_ = dict(abort=str(ex_)[:300])
MON["on"] = False
print("DROP", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:250]) for k_, v_ in (o_ or {}).items()}, flush=True)
print("after", state(), "LOCK", list(LOCK), "HELD", HELD, "touch", contact_report(), "fell", fallen(), flush=True)
print("check", item_check(nm_), flush=True)
print(look3("jacket_drop"), flush=True)
