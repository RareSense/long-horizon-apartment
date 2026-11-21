ZZ = finish_put("r195i3_paper", "left")
print("FINISH", {k_: (v_ if k_ != "route" else {kk: vv for kk, vv in (v_ or {}).items() if kk in ("ckpt", "pos")}) for k_, v_ in ZZ.items()}, flush=True)
print("SAY", say_item(), "HELD", {s_: HOLD.holding(s_) for s_ in SIDES}, "fell", fallen(), flush=True)
