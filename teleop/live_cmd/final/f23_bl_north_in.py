zz_n = "r117i1_blanket"; zz_h = laundry_body()
BC["stage"] = "carry"; CARRY_JOINTS = True
print("ck", ck_save("bc_blanket_at_north_pre", kind="act"), flush=True)
zz_r = bigcloth_into(zz_n, s1="right", start="step_in", stop_after="strand")
for r_ in zz_r:
    print("RESULT", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:200]) for k_, v_ in r_.items() if k_ != "look"}, flush=True)
print("inside", in_container(zz_n, zz_h), "out", bc_out(zz_n, zz_h), "state", state(), "touch", contact_report(), "LOCK", list(LOCK), "HELD", HELD, "fell", fallen(), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print(n_, item_check(n_), flush=True)
print("look3", look3("bl_north_strand"), flush=True)
