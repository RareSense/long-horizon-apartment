# session settings under test (AI-operated): reload the code of this checkout and set the walking settings
exec(open(r"E:\urc_gait\scripts\home\gait\gait_test.py", encoding="utf-8").read())
gt_reload_session()
hot_reload(r"E:\urc_gait\scripts\home\skills.py", ["_settle_stop", "_turn_on_spot", "walk", "_leg_by_anchor", "_leg_by_anchor_xy"])
exec(open(r"E:\urc_gait\scripts\home\live\teleop.py", encoding="utf-8").read())
ARM_TUCK = dict(pitch=0.05, roll=0.15, yaw=0.0, elbow=0.6)
TURN_BY_REF, TURN_TOL_REF, TURN_W_MIN = True, 0.01, 0.08
WALK_BY_ANCHOR, ANCHOR_LEG_MAX, V_ANCHOR = True, 1.2, 0.18
SHORT_NO_TURN, V_SHORT = 0.45, (0.12, 0.06)
GT_PRE = lambda: op.run(1.5)        # the loaded checkpoints stand 16 deg rolled (old lean bug): let the upright target level first
PLAN_TOL, V_ANCHOR_CARRY = 0.015, 0.12


def GT_PRE():
    # the loaded checkpoints stand 16 deg rolled (old lean bug) and some were saved while the gait still settled:
    # stand, let the upright target level and the centre of mass centre, then measure
    op.run(4.0, until=_standing)
    op.run(1.5)
