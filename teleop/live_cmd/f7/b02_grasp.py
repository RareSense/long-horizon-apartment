exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
zz_n = "r116i1_coat_pile"
MON["trace"] = []
zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(0.0, 0.30))
print("RESULT", zz_r, flush=True)
print("trace", MON["trace"][::3], flush=True)
print("grasp look", BC.get("grasp_look"), "state", state(), "touch", contact_report(), "kit", kit_mem(), flush=True)
print("look3", look3("coat_grasped"), flush=True)
