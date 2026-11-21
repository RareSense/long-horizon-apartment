exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\gait3\setup.py", encoding="utf-8").read())
print("GAIT", gt_reload_gait(hold=False, plan=True))
GREG = dict(tuck=True, only=["turn_table_right", "turn_table_left", "turn_0237_left", "leg_table_back", "short_diag_0.3", "leg_onto_rug_fwd", "inplace_table_8s"])
exec(open(r"E:\urc_gait\scripts\home\gait\gait_regress.py", encoding="utf-8").read())
