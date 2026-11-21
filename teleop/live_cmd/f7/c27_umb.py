print(floor_first(["r107i1_umbrella"])[:3], "spot", (DESC.get("spots") or {}).get("r107i1_umbrella"), "box", [np.round(v_, 3).tolist() for v_ in obj_box(body_of("r107i1_umbrella"))], flush=True)
zz_r = go_item()
print("ITEM", {k_: v_ for k_, v_ in zz_r.items() if k_ != "route"}, flush=True)
for e_ in EVENTS[-5:]:
    print({k_: (str(v_)[:140]) for k_, v_ in e_.items()}, flush=True)
print("umbrella", np.round(centre(body_of("r107i1_umbrella")), 3).tolist(), "state", state(), "kit", kit_mem(), flush=True)
