# AI-operated (Fable escalation, scooter r126): second move: turn 15 deg left and a first 10 cm step toward (-1.75,-0.50)
# (mostly to the robot's right: the first sideways step with the scooter hanging; watched).
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
mvto("m2", turn=15.0, to=(-1.75, -0.50), step=0.10)
topview("c06")
print("mem", mem(), flush=True)
