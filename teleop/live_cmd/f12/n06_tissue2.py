MON["on"] = False
CREEPERS.add(body_of("r100i1_towel"))   # it slid 8.7 cm by itself (leans on object_0231 at z 0.1; robot 1.08 m away), still after
tb_ = body_of("r158i1_tissue")
ZZ = surf_item("r158i1_tissue")
if ZZ.get("ok") and inside(tb_, body_of("rubbish_bin")):
    print("DONE", item_done_auto("r158i1_tissue", dict(status="done", how="library tidy_surface + bin drop (AI-operated)")), flush=True)
