exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
LD = "0537_start_scout_start"; exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\sc\ld.py", encoding="utf-8").read())
zz_b = body_of("r120i1_duck"); mon_start(target=zz_b)
try:
    back_off_container(); walk_tight(DUCK_APPROACH)
    print("PICK", pick_at(zz_b, "left", DUCK_STANCE, duck_head_plan(zz_b)), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
