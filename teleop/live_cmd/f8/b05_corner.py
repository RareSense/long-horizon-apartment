exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f8\zz_corner.py", encoding="utf-8").read())
for k_ in range(4):
    for sd_ in ("left", "right"):
        print(k_, sd_, [dict(stance=np.round(p_["stance"], 3).tolist(), free=p_["free"]) for p_ in zz_corner_plan(k_, sd_)], flush=True)
