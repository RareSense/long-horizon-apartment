# AI-operated (Fable escalation, scooter r126): at the set-down start (-1.90, 0.55) facing south. Checkpoint; the rear
# wheel down onto the floor; the first leg of the skill's set-down walk.
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
print("ck", ck_save("fsc_setdown_start", kind="act", info=dict(note="scooter hanging, robot at the set-down start facing south (AI-operated)")), flush=True)
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    latc(want=-0.26)
    sd_rep("start")
    sd_touch()
    print("leg ->", sd_leg("1"), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
    sd_rep("abort")
views("e00")
