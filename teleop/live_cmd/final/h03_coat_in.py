zz_n = "r116i1_coat_pile"; zz_h = laundry_body()
BC["stage"] = "carry"; CARRY_JOINTS = True
print("ck", ck_save("bc_coat_at_north_pre", kind="act"), flush=True)
zz_r = bigcloth_into(zz_n, s1="right", start="step_in", stop_after="strand")
for r_ in zz_r:
    print("RESULT", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:200]) for k_, v_ in r_.items() if k_ != "look"}, flush=True)
print("inside", in_container(zz_n, zz_h), "out", bc_out(zz_n, zz_h), "state", state(), "touch", contact_report(), "LOCK", list(LOCK), "HELD", HELD, "fell", fallen(), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print(n_, item_check(n_), flush=True)
print("look3", look3("coat_north_strand"), flush=True)
if not cloth_held("left") and zz_r and zz_r[-1].get("stage") == "strand" and not zz_r[-1].get("ok"):
    print("between pads now", len(bc_w(zz_n).caught("left")), flush=True)
    zz_c = bc_close_lock(zz_n, "left")
    print("manual close", zz_c, "held L/R", cloth_held("left"), cloth_held("right"), flush=True)
    print("look", look_hand("left", "coat_strand_closed"), flush=True)
