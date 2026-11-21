print("route head", [item_name(s_) for s_ in ROUTE[POS:]], "done", len(DONE), flush=True)
for n_ in ("r93i1_nugget", "r83i1_sponges"):
    b_ = body_of(n_); print(n_, np.round(centre(b_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(b_)], flush=True)
for st_ in INFO["static"]:
    for bx_ in st_.get("boxes", [])[:2]:
        try:
            c_ = np.asarray(bx_["c"], float); s_ = np.asarray(bx_["s"], float)
        except Exception:
            continue
        if 1.0 < c_[0] < 3.5 and -1.5 < c_[1] < 1.0:
            print("static", st_["name"], st_.get("cls"), "c", np.round(c_[:2], 2).tolist(), "size", np.round(s_[:2], 2).tolist(), "z1", round(float(bx_.get("z1", 0)), 2), flush=True)
