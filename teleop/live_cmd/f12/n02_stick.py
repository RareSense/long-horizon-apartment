MON["on"] = False
sb_ = body_of("r154i1_stick"); lo_, hi_ = obj_box(sb_)
print("stick", np.round(centre(sb_), 3).tolist(), np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "mass", round(float(m.body_mass[m.body(sb_).id]), 3), "dest", place_for(sb_), flush=True)
ZZ = surf_item("r154i1_stick")
if ZZ.get("ok"):
    print("DONE", item_done_auto("r154i1_stick", dict(status="done", how="library tidy_surface (AI-operated)")), flush=True)
