for n_ in ("r125i1_flat", "r125i2_flat", "r105i1_shoe", "r105i2_shoe", "r124i1_sandal", "r122i1_croc", "r123i1_slipper"):
    b_ = body_of(n_)
    print(n_, DESC["destinations"].get(n_), "spot", (OVR["spots"].get(n_) if "OVR" in globals() else None), (DESC.get("spots") or {}).get(n_), "at", np.round(centre(b_), 3).tolist(), "box", [np.round(v_, 3).tolist() for v_ in obj_box(b_)], flush=True)
