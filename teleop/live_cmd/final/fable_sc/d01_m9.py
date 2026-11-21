# AI-operated (Fable escalation, scooter r126): one backward move with the left fingers pitched 12 deg tips-down before it
# (test: does the bar stop creeping toward the left palm?). Bar first back to 0.25 right of the pelvis line.
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
PF = (-1.89, 0.61)
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    latc(want=-0.25)
    prepitch(-12.0)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
mvto("m9", turn=float(np.degrees(wrapa(np.radians(-90.0) - base()[1]))), to=PF, step=0.15)
topview("d01")
