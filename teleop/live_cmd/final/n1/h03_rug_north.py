exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\rug_lib.py", encoding="utf-8").read())
rec.still_every = 300
for nm_, sd_, yw_ in (("r193i3_toy_piece", "left", 90.0), ("r193i1_toy_piece", "left", 90.0)):
    if nm_ in DONE:
        continue
    try:
        ok_ = rug_toy_at(nm_, sd_, yw_)
    except Exception:
        import traceback as _tb; print("EXC", _tb.format_exc()[-800:], flush=True); ok_ = False
    print("RUG_RESULT", nm_, ok_, "done", len(DONE), "rec", rec.n, "kit", kit_mem(), flush=True)
    if not ok_ or fallen():
        break
