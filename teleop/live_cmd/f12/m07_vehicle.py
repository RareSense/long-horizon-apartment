T5 = toy_trip("r191i1_toy_vehicle")
print("TRIP", T5.get("in"), (T5.get("done") or {}).get("ckpt"), T5.get("abort_pick") or (T5.get("put") or {}).get("abort"), T5.get("pick"), "state", state(), "fell", fallen(), flush=True)
