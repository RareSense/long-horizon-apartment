ZZ = go_item("r121i1_jacket")
print("HELD", {s_: HOLD.holding(s_) for s_ in SIDES}, "LOCK", list(LOCK) if "LOCK" in globals() else None, "fell", fallen(), "touch", contact_report(), flush=True)
print("jacket check", item_check("r121i1_jacket"), flush=True)
print("SAY", say_item(), flush=True)
