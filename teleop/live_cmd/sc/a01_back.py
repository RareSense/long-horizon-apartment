MON["on"] = False
for k_ in range(2):
    r_ = tmove(fwd=-0.10, carry=("left",), tag="off_bin_tall")
    print("step", k_, state(), "touch", contact_report()["body"], "fell", fallen(), flush=True)
    if fallen():
        break
refresh_jointed_footprints()
rest_hands(SIDES)
op.run(4.0, until=_standing); op.run(1.5)
print("after", state(), "fell", fallen(), flush=True)
print(look3("sc_start"), flush=True)
for n_ in ("r120i1_duck", "r105i1_shoe", "r105i2_shoe", "r107i1_umbrella", "r100i1_towel", "r186i1_basket", "r133i1_laundry_basket", "r119i1_mat"):
    b_ = body_of(n_)
    lo_, hi_ = obj_box(b_)
    print(n_, "c", np.round(centre(b_), 3).tolist(), "box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "kg", round(float(m.body_mass[m.body(b_).id]), 3), "->", DESC["destinations"].get(n_), (DESC.get("spots") or {}).get(n_), flush=True)
print("kit", kit_mem(), flush=True)
