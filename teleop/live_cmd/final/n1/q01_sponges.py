rec.still_every = 300
print("ck", ck_save("n1_pre_sponges", kind="act", info=dict(note="before the sponges (AI-operated)")), flush=True)
try:
    zz_ok = ITEM_FN["r83i1_sponges"](0)
except Exception:
    import traceback as _tb; print("EXC", _tb.format_exc()[-1200:], flush=True); zz_ok = False
print("ZZ_OK", zz_ok, "state", state(), "fell", fallen(), "done", len(DONE), "rec", rec.n, "kit", kit_mem(), flush=True)
print(look3("n1_sponges_end"), flush=True)
