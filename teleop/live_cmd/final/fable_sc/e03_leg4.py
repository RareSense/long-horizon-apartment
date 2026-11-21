# AI-operated (Fable escalation, scooter r126): set-down leg 4 (no trim).
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    print("leg ->", sd_leg("4", trim=False), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
    sd_rep("abort")
print("LOOK", look3("fsc_e03"), flush=True)
views("e03")
