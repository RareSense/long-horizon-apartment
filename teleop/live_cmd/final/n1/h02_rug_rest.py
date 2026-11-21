rec.still_every = 300
for nm_, sd_ in (("r192i1_ball", "right"), ("r193i2_toy_piece", "left"), ("r193i1_toy_piece", "left"), ("r193i3_toy_piece", "left")):
    if nm_ in DONE:
        continue
    try:
        ok_ = rug_toy(nm_, sd_)
    except Exception:
        import traceback as _tb; print("EXC", _tb.format_exc()[-800:], flush=True); ok_ = False
    print("RUG_RESULT", nm_, ok_, "done", len(DONE), "rec", rec.n, "kit", kit_mem(), flush=True)
    if not ok_ or fallen():
        break
