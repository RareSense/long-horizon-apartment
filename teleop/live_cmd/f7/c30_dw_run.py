exec(open(r"E:\urc_cloth\scripts\home\kitchen_skills.py", encoding="utf-8").read())
CREEPERS |= {body_of(n_) for n_ in ("r69i1_scrap", "r69i2_scrap", "r69i3_scrap", "r69i4_scrap")}
r = step_mon()
print("STEP", str(r)[:900], flush=True)
print("state", state(), "done", len(DONE), "next", [item_name(s_) for s_ in ROUTE[POS:POS + 3]], "kit", kit_mem(), flush=True)
print("look", look3("after_close_dishwasher"), flush=True)
