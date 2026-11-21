zz_names = ["r192i1_ball", "r193i1_toy_piece", "r193i3_toy_piece", "r193i2_toy_piece", "r193i4_toy_piece", "r191i1_toy_vehicle"]
zz_cb = body_of("r186i1_basket")
print("basket", [np.round(v_, 3).tolist() for v_ in obj_box(zz_cb)], flush=True)
zz_bs = [body_of(n_) for n_ in zz_names]
for n_, b_ in zip(zz_names, zz_bs): print(n_, b_, np.round(centre(b_), 2).tolist(), flush=True)
hub_ = plan_hub(zz_bs, cont=zz_cb)
print("HUB", None if hub_ is None else dict(c=np.round(hub_["c"], 3).tolist(), covered=[INFO["bodies"][n].get("display", n) for n in hub_["covered"]], stances=[np.round(s_, 2).tolist() for s_, r_ in hub_["stances"]]), flush=True)
hub2 = with_tight(lambda: plan_hub(zz_bs, cont=zz_cb))
print("HUB tight", None if hub2 is None else dict(c=np.round(hub2["c"], 3).tolist(), covered=[INFO["bodies"][n].get("display", n) for n in hub2["covered"]], stances=[np.round(s_, 2).tolist() for s_, r_ in hub2["stances"]]), flush=True)
def zz_map():
    g_ = room_grid(())
    for y_ in np.arange(0.3, -2.45, -0.1):
        print(f"{y_:5.1f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(-6.0, -1.9, 0.1)), flush=True)
print("TIGHT x -6.0..-2.0", flush=True); with_tight(zz_map)
