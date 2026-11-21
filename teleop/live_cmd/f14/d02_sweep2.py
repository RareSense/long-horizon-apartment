print("GARMENTS keys", list(GARMENTS.keys()) if "GARMENTS" in globals() else None, flush=True)
cands_ = [n_ for n_ in INFO["bodies"] if any(k_ in str(INFO["bodies"][n_].get("display", "")) for k_ in ("r133", "hamper", "laundry", "r186", "basket", "r119"))]
print("containers", [(n_, INFO["bodies"][n_].get("display")) for n_ in cands_], flush=True)
for st_ in RESULT.get("steps", []):
    s0_ = st_.get("step")
    if s0_ and (s0_[0] in ("garments", "close_dishwasher") or "dishwasher" in str(s0_)):
        print("STEP", str(s0_)[:200], "rec", str(st_.get("rec") or st_.get("result"))[:300], flush=True)
try:
    print("dw names", dw_names(), flush=True)
except Exception as ex_:
    print("dw", ex_)
