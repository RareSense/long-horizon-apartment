CK_STATE["item"] = "000_start_clean"
P_START = ck_save("clean", kind="start", info=dict(note="FINAL clean episode start (AI-operated): seg3 0000_item_start + 26 removed off-map at frame 0 (REMOVED_FOR_40.json incl. removed_final)", removed=RM_OUT))
print("START", P_START, "frame", rec.n, flush=True)
print(look3("final_start"), flush=True)
print("srec frames", rec.srec.frames, "chunk idx", rec.srec.ci, flush=True)
