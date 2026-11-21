op.run(2.0)
for g_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print("check", item_check(g_), flush=True)
print("DONE", tele_item_done("r121i1_jacket", note="go_item (tidy_garment: try 2 held, tight stance) hit the 240 s item cap before the drop; finished by drop_in_cloth from the hamper's north side (raised to 1.33, over the opening, open): inside 1.0, below rim 1.0 (AI-operated)"), flush=True)
print("SAY", say_item(), flush=True)
