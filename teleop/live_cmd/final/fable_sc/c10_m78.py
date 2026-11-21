# AI-operated (Fable escalation, scooter r126): moves 7 and 8: the last 6.7 deg to face south, backward (north) toward the
# set-down start (-1.89, 0.61).
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
PF = (-1.89, 0.61)
r_ = mvto("m7", turn=float(np.degrees(wrapa(np.radians(-90.0) - base()[1]))), to=PF, step=0.15)
if r_ is not None and r_["along"]["left"] < 0.135:
    mvto("m8", turn=float(np.degrees(wrapa(np.radians(-90.0) - base()[1]))), to=PF, step=0.15)
topview("c10")
print("mem", mem(), flush=True)
