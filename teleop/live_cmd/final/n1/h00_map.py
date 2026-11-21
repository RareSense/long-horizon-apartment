rec.still_every = 300
print("state", state(), "held", {s_: HOLD.holding(s_) for s_ in SIDES}, flush=True)
for st_ in INFO["static"]:
    for bx_ in st_.get("boxes", [])[:1]:
        try:
            c_ = np.asarray(bx_["c"], float); s_ = np.asarray(bx_["s"], float)
        except Exception:
            continue
        if -5.0 < c_[0] < -2.3 and -2.6 < c_[1] < 0.2:
            print("static", st_["name"], st_.get("cls"), "c", np.round(c_[:2], 2).tolist(), "size", np.round(s_[:2], 2).tolist(), "z1", round(float(bx_.get("z1", 0)), 2), flush=True)
for n_ in ("r145i1_coffee_table", "r166i1_ottoman", "r185i1_megabloks_bag"):
    b_ = body_of(n_)
    if b_: print(n_, [np.round(v_, 2).tolist() for v_ in obj_box(b_)], flush=True)
