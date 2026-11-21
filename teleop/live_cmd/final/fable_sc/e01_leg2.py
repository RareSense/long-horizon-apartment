# AI-operated (Fable escalation, scooter r126): set-down leg 2 (no trim after it: the trim after leg 1 lifted the bar 6 mm
# and the unloaded wheel slid 4.5 cm back under the bar).
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    print("leg ->", sd_leg("2", trim=False), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
    sd_rep("abort")
print("LOOK", look3("fsc_e01"), flush=True)
