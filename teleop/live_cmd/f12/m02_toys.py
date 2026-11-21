TT = []
for nm_ in ("r192i1_ball", "r193i2_toy_piece", "r193i1_toy_piece", "r193i3_toy_piece"):
    r_ = toy_trip(nm_)
    TT.append((nm_, r_.get("in"), (r_.get("done") or {}).get("ckpt"), r_.get("abort_pick") or (r_.get("put") or {}).get("abort")))
    print("TRIP", TT[-1], "kit", kit_mem(), flush=True)
    if r_.get("fell") or not r_.get("in"):
        break
print("TT", TT, flush=True)
