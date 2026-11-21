ck_load(os.path.join(RUN, "checkpoints", "0368_item_r190i1_stocking")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
print("RELOADED 0368 rec", rec.n, state(), "route", item_name(ROUTE[POS]), "done", len(DONE), flush=True)
try:
    zz_ok = ITEM_FN["r120i2_duck"](0)
except Exception:
    import traceback as _tb; print("EXC", _tb.format_exc()[-1200:], flush=True); zz_ok = False
print("ZZ_OK", zz_ok, "state", state(), "fell", fallen(), "rec", rec.n, "done", len(DONE), flush=True)
print(look3("n1_duck_end2"), flush=True)
