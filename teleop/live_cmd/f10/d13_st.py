print("box sample", str(INFO["static"][0]["boxes"][:1])[:300], flush=True)
for st_ in INFO["static"]:
    for bx_ in st_.get("boxes", []):
        try:
            c_ = np.asarray(bx_.get("c") if isinstance(bx_, dict) else bx_[0], float); s_ = np.asarray(bx_.get("s") if isinstance(bx_, dict) else bx_[1], float)
        except Exception:
            continue
        r_ = float(np.max(s_[:2]))
        if -6.1 < c_[0] + r_ and c_[0] - r_ < -4.6 and -2.15 < c_[1] + r_ and c_[1] - r_ < -1.2:
            print(st_["name"], st_.get("cls"), "c", np.round(c_, 2).tolist(), "s", np.round(s_, 2).tolist(), flush=True)
for b_ in INFO["bodies"]:
    try: c_ = centre(b_)
    except Exception: continue
    if -6.2 < c_[0] < -4.6 and -2.4 < c_[1] < -1.0: print("loose", b_, INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist(), [np.round(v_, 2).tolist() for v_ in obj_box(b_)], flush=True)
