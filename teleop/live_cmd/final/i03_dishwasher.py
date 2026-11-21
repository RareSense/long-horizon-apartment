# close_dishwasher (racks r33 in, door r32 shut): kitchen_skills.step_mon (the kitchen agent's proven call). AI-operated
exec(open(r"E:\urc_final\scripts\home\kitchen_skills.py", encoding="utf-8").read())
CREEPERS |= {body_of(n_) for n_ in ("r69i1_scrap", "r69i2_scrap", "r69i3_scrap", "r69i4_scrap") if body_of(n_)}
print("ROUTE[POS]", ROUTE[POS], flush=True)
r = step_mon()
print("STEP", str(r)[:900], flush=True)
if "refresh_jointed_footprints" in globals():
    refresh_jointed_footprints()
print("check", item_check("close_dishwasher"), "state", state(), "done", len(DONE), "next", [item_name(s_) for s_ in ROUTE[POS:POS + 3]], flush=True)
print("look", look3("after_close_dishwasher"), flush=True)
print("SAY", say_item(), flush=True)
