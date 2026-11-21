RUN = r"C:\Users\raresense\sim_home\runs\1120_0110_gait3_fresh_AI_operated"
exec(open(r"E:\urc_gait\scripts\home\gait\g_session.py", encoding="utf-8").read())
print("FRESH defaults: plan", ts.loco.g.get("plan"), "hold", ts.loco.g.get("hold"), "ARM_TUCK", ARM_TUCK, "TURN_BY_REF", TURN_BY_REF, "WALK_BY_ANCHOR", WALK_BY_ANCHOR, "PLAN_TOL", PLAN_TOL, "V_ANCHOR_CARRY", V_ANCHOR_CARRY, "TUCK_JOINTS", TUCK_JOINTS)
print("FRESH gait", {k_: v_ for k_, v_ in ts.loco.g.items() if k_.startswith("plan")})


def GT_PRE():
    op.run(4.0, until=_standing)
    op.run(1.5)


GREG = dict(tuck=False, only=["turn_table_left", "turn_0237_right", "t15_0237", "f12_0237", "r12_table", "leg_off_rug_back", "carry_back_0.5"])
exec(open(r"E:\urc_gait\scripts\home\gait\gait_regress.py", encoding="utf-8").read())
