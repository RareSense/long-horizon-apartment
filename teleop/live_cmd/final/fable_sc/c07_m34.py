# AI-operated (Fable escalation, scooter r126): moves 3 and 4: turn 15 deg left each, 14 cm steps toward (-1.75,-0.50).
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
if mvto("m3", turn=15.0, to=(-1.75, -0.50), step=0.14) is not None:
    mvto("m4", turn=15.0, to=(-1.75, -0.50), step=0.14)
topview("c07")
print("mem", mem(), flush=True)
