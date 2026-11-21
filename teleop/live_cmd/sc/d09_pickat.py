exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
LD = "0290_act_rest_hands"; exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\sc\ld.py", encoding="utf-8").read())
zz_b = body_of("r120i1_duck"); mon_start(target=zz_b)
try:
    print("PICK", pick_at(zz_b, "left", DUCK_STANCE, duck_head_plan(zz_b)), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "duck", np.round(centre(zz_b), 3).tolist(), "touch", finger_touch("left", zz_b), flush=True)
print(look3("d09_pick_at"), flush=True)
