exec(open(r"E:\urc_home\scripts\home\live\ops.py", encoding="utf-8").read())
zz_u = body_of("r106i1_umbrella")
C_, c_, z0_, z1_ = flat_corners(zz_u)
print("corners", np.round(C_, 3).tolist(), "c", np.round(c_, 3).tolist(), "z", round(z0_, 3), round(z1_, 3), flush=True)
for k_ in range(4):
    for sd_ in ("left", "right"):
        print(k_, sd_, [dict(stance=np.round(p_["stance"], 3).tolist(), free=p_["free"]) for p_ in corner_pinch_plan(zz_u, k_, sd_)], flush=True)
