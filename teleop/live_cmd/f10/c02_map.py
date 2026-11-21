zz_b = body_of("r139i1_toy_car")
for rb0_ in (0.24, 0.20):
    g_ = with_tight(lambda: room_grid((zz_b,)), rb0=rb0_, rf0=0.12)
    print("rb0", rb0_, "x from -2.6 step 0.1")
    for yy_ in np.arange(-1.0, -2.75, -0.1):
        print(f"{yy_:6.2f}", "".join("." if g_.free(np.array([xx_, yy_])) else "#" for xx_ in np.arange(-2.6, 0.01, 0.1)), flush=True)
for st_ in INFO["static"]:
    try:
        lo_, hi_ = np.asarray(st_["lo"]), np.asarray(st_["hi"])
    except Exception:
        continue
    if lo_[0] < -0.6 and hi_[0] > -2.2 and lo_[1] < -1.6 and hi_[1] > -2.8:
        print("static", st_["name"], np.round(lo_, 2).tolist(), np.round(hi_, 2).tolist(), flush=True)
print("keys", list(INFO["static"][0].keys())[:12], flush=True)
for b_ in INFO["bodies"]:
    try: c_ = centre(b_)
    except Exception: continue
    if -2.4 < c_[0] < -0.4 and -2.8 < c_[1] < -1.2: print("loose", b_, INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist(), flush=True)
