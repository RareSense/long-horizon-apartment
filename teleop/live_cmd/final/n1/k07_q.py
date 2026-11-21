pb_ = body_of("r149i1_pouch"); C_, c_, z0_, z1_ = flat_corners(pb_)
print("pouch", np.round(centre(pb_), 3).tolist(), "corners", np.round(C_, 3).tolist(), flush=True)
for k_ in range(4):
    for sd_ in SIDES:
        print(k_, sd_, [dict(stance=np.round(p_["stance"], 3).tolist(), free=p_["free"]) for p_ in corner_pinch_plan(pb_, k_, sd_, 0.018)], flush=True)
