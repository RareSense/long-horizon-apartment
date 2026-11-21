BC["stage"] = "free1"
ZZ_START = "fold"; ZZ_STOP = "fold"
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g07_stage.py", encoding="utf-8").read())
print("fold look", BC.get("fold_look"), flush=True)
if "right" in LOCK:
    print("right held uv", np.round(zz_uv()[LOCK["right"][1]], 2).tolist(), flush=True)
