ZZ_RECORD = True
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g42_done.py", encoding="utf-8").read())
print("after: route item", item_name(ROUTE[POS]) if POS < len(ROUTE) else None, "DONE tail", DONE[-4:], "state", state(), "fallen", fallen(), "LOCK", dict(LOCK), "HELD", dict(HELD), flush=True)
print("item checkpoints", sorted(n_ for n_ in os.listdir(CK_DIR) if "item_r117i1" in n_), flush=True)
