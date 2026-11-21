zz_b = body_of("r120i1_duck"); sb_ = body_of("r130i1_light_saber")
print("duck", np.round(centre(zz_b), 3).tolist(), "held", HOLD.holding("left"), "pad", np.round(pad_mid("left"), 3).tolist(), "state", state(), flush=True)
print("saber hull", [np.round(v_, 3).tolist() for v_ in obj_box(sb_)], "corners", np.round(flat_corners(sb_)[0], 3).tolist() if flat_corners(sb_) else None, flush=True)
print("basket rect", obj_rect(body_of("r186i1_basket")).c.round(3).tolist(), flush=True)
