ZZ = go_item("r131i1_knit_hat")
print("HELD", {s_: HOLD.holding(s_) for s_ in SIDES}, "fell", fallen(), "touch", contact_report(), flush=True)
try:
    zz_hb = place_for(body_of("r131i1_knit_hat")); print("hat in", zz_hb, in_container("r131i1_knit_hat", zz_hb), flush=True)
except Exception as ex_:
    print("in_container ERR", str(ex_)[:200], flush=True)
print("SAY", say_item(), flush=True)
