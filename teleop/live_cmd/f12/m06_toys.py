T4 = toy_trip("r193i3_toy_piece")
print("TRIP", T4.get("in"), (T4.get("done") or {}).get("ckpt"), T4.get("abort_pick") or (T4.get("put") or {}).get("abort"), flush=True)
