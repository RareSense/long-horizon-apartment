ZZ_K = 0
try:
    zz_ok = ITEM_FN["r120i2_duck"](ZZ_K)
except Exception:
    import traceback as _tb; print("EXC", _tb.format_exc()[-1200:], flush=True); zz_ok = False
print("ZZ_OK", zz_ok, "state", state(), "fell", fallen(), "rec", rec.n, "done", len(DONE), flush=True)
print(look3("n1_duck_end"), flush=True)
