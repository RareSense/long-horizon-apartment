zz_b = body_of("r196i1_plastic_bag")
C_, c_, z0_, z1_ = flat_corners(zz_b)
print("bag corners", np.round(C_, 3).tolist(), "c", np.round(c_, 3).tolist(), "z", round(z0_, 4), round(z1_, 4), "zpad", round(z0_ + 0.4 * (z1_ - z0_), 4), flush=True)
for k_ in range(4):
    for sd_ in ("left", "right"):
        print(k_, sd_, [dict(stance=np.round(p_["stance"], 3).tolist(), free=p_["free"]) for p_ in corner_pinch_plan(zz_b, k_, sd_)], flush=True)
