for n_ in ["r105i1_shoe", "r105i2_shoe", "r107i1_umbrella", "r83i1_sponges", "r120i1_duck", "r186i1_basket", "r192i1_ball", "r193i1_toy_piece", "r193i2_toy_piece", "r193i3_toy_piece", "r193i4_toy_piece", "r191i1_toy_vehicle", "r159i1_door", "r154i1_stick", "r158i1_tissue", "r87i1_wrapper", "r93i1_nugget", "r100i1_towel", "r123i1_slipper"]:
    b_ = body_of(n_)
    try:
        print(n_, "at", np.round(centre(b_), 2).tolist(), "->", DESC["destinations"].get(n_), (DESC.get("spots") or {}).get(n_), "done" if n_ in DONE else "", flush=True)
    except Exception as ex_:
        print(n_, "ERR", str(ex_)[:80], flush=True)
print("route", [item_name(s_) for s_ in ROUTE[POS:]], flush=True)
print("kit", kit_mem(), flush=True)
