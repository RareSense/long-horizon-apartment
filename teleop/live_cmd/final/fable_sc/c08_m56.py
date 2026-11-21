# AI-operated (Fable escalation, scooter r126): the bar back to 0.27 right of the pelvis line, then moves 5 and 6:
# turn 15 deg left each, steps toward (-1.75,-0.50) and on toward the set-down start (-1.89, 0.61).
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
latc()
if mvto("m5", turn=15.0, to=(-1.75, -0.50), step=0.14) is not None:
    mvto("m6", turn=15.0, to=(-1.77, -0.36), step=0.14)
topview("c08")
print("mem", mem(), flush=True)
