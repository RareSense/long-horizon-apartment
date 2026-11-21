p_, _ = base()
for s_ in ROUTE[POS:]:
    n_ = item_name(s_); b_ = body_of(n_)
    try:
        c_ = np.round(centre(b_), 2).tolist() if b_ in INFO["bodies"] else (np.round(garment_box(n_)[0], 2).tolist() if n_ in GARMENTS else None)
    except Exception as ex_:
        c_ = str(ex_)[:30]
    print(n_, "->", DESC["destinations"].get(n_), c_, flush=True)
print("mat", np.round(obj_box(body_of("r119i1_doormat"))[0], 2).tolist() if body_of("r119i1_doormat") in INFO["bodies"] else [k_ for k_ in INFO["bodies"] if "119" in str(INFO["bodies"][k_].get("display", ""))], flush=True)
