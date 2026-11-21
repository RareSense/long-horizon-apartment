zz_w = GARMENTS["r131i1_knit_hat"]["w"]
print("in_container", in_container("r131i1_knit_hat", zz_hb), "at_fingers", zz_w.at_fingers("left"), "LOCK", LOCK.get("left"), "jaw", jaw_target.get("left"))
print("left ee", np.round(ts.ee_pose("left")[0], 3).tolist(), "pad", np.round(pad_mid("left"), 3).tolist(), "rect c", np.round(obj_rect(zz_hb).c, 3).tolist(), np.round(obj_rect(zz_hb).h, 3).tolist())
print("events", EVENTS[-4:], flush=True)
