print("rec", rec.n, "route head", [item_name(s_) for s_ in ROUTE[POS:POS + 8]], flush=True)
for n_ in ("r190i1_stocking", "r130i1_light_saber", "r120i2_duck", "r125i1_flat", "r175i1_cardboard_box", "r186i1_basket", "r178i1_ball", "r179i1_toy_pouch"):
    b_ = body_of(n_)
    if b_ is None:
        print(n_, "no body", flush=True); continue
    lo_, hi_ = obj_box(b_); print(n_, np.round(centre(b_), 3).tolist(), "box", np.round(lo_[:2], 2).tolist(), np.round(hi_[:2], 2).tolist(), "dest", DESC["destinations"].get(n_), flush=True)
A_, ax_, a_, bid_, j_ = hinge_axis("r159i1_door"); print("tv door q", round(float(d.qpos[a_]), 3), "box", [np.round(v_, 2).tolist() for v_ in obj_box(m.body(bid_).name)], flush=True)
print("stocking garment?", "r190i1_stocking" in GARMENTS if "GARMENTS" in globals() else None, flush=True)
