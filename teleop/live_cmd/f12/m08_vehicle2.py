exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\basket_put.py", encoding="utf-8").read())
vb_ = body_of("r191i1_toy_vehicle"); lo_, hi_ = obj_box(vb_)
print("vehicle box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "basket", [np.round(v_, 3).tolist() for v_ in obj_box(body_of("r186i1_basket"))], flush=True)
BASKET_Z = 0.21
T6 = toy_trip("r191i1_toy_vehicle", note=" (2nd try: released lower, pads 0.21 m; the 1st drop from 0.30 m ended 0.38 m north of the basket on the floor)")
print("TRIP", T6.get("in"), (T6.get("done") or {}).get("ckpt"), T6.get("abort_pick") or (T6.get("put") or {}).get("abort"), "at", np.round(centre(vb_), 3).tolist(), flush=True)
