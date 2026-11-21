R2 = bin_drop("r158i1_tissue", "right")
print("BIN", R2, flush=True)
if R2.get("in") and not R2.get("fell"):
    print("DONE", item_done_auto("r158i1_tissue", dict(status="done", how="tidy_surface failed twice (pads short; a fingertip on the sofa seat 68 N); AI teleop: stepped 6 cm closer, corner pinch 1.8 cm in at the nearest corner, grasp-QC guard passed (both fingers, no rise in the close), hold_on, lift 10 cm; put_away to the bin (AI-operated)")), flush=True)
print(look3("f12_tissue_bin"), flush=True)
