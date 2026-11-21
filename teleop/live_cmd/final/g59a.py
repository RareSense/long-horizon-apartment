BC["stage"] = "lower_release"
ZZ_START = "retract"; ZZ_STOP = "retract"
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g56_stage.py", encoding="utf-8").read())
print("jaws", {s_: round(float(jaw(s_)), 4) for s_ in SIDES}, "LOCK", dict(LOCK), "HELD", dict(HELD), "CARRY_JOINTS", CARRY_JOINTS, "asleep", bool(zz_w().asleep), flush=True)
print("look3", look3("g59_retract"), flush=True)
