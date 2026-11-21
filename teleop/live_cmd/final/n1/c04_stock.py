print("ck", ck_save("n1_start_bag_kept", kind="act", info=dict(note="3161 reloaded, plastic bag given up and left in place (route only); AI-operated")), "rec", rec.n, flush=True)
try:
    zz_ok = ITEM_FN["r190i1_stocking"](0)
except Exception:
    import traceback as _tb; print("EXC", _tb.format_exc()[-1200:], flush=True); zz_ok = False
print("ZZ_OK", zz_ok, "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
