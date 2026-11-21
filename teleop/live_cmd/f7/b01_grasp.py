exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
zz_n = "r116i1_coat_pile"
mon_start(target=None)
try:
    print("back_off", back_off_container(), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(0.0, 0.30))
print("RESULT", [{k_: v_ for k_, v_ in r_.items()} for r_ in zz_r], flush=True)
print("grasp look", BC.get("grasp_look"), "state", state(), "touch", contact_report(), "kit", kit_mem(), flush=True)
print("look3", look3("coat_grasped"), flush=True)
