# AI-operated (Fable escalation, scooter r126): the open jaws already straddle the bar after the step in: pads to their
# places on it (seat0), slowly; close; grip check. No lift.
mon_start(target=sc_); MON["t_max"] = 6000.0
try:
    PRE_ACTION("fsc_seat_on_bar", dict(note="open jaws straddle the bar after the step in (AI-operated)"))
    tg_, Q_, F_ = sh_targets(sc_, back=SH["seat0"])
    e2_ = both_move(tg_, Q_, speed=0.04, tol=0.005)
    print("on_err", e2_, flush=True)
    diag("on", tg_)
    print("in_jaws open", sh_in_jaws(sc_), "seat", sh_seat(sc_), flush=True)
    views("c01_open")
    PRE_ACTION("fsc_close", dict(note="pads at their places on the bar, open (AI-operated)"))
    for s_ in SIDES:
        jaw_force[s_] = 14.0; jaw_target[s_] = 0.0
    op.run(0.8)
    g_ = {s_: grip_check(s_, None, min_gap=0.0015) for s_ in SIDES}
    ok_, t_, e_, a_ = sh_in_jaws(sc_)
    print("GRIP ok", bool(ok_ and all(g_[s_]["ok"] for s_ in SIDES)), g_, "touch", t_, "pad_to_bar", e_, "along", a_, flush=True)
    print("seat", sh_seat(sc_), flush=True)
    diag("closed")
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
views("c01")
print("mem", mem(), flush=True)
