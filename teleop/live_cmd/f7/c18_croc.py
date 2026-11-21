MON["trace"] = []
zz_r = go_item()
print("ITEM", {k_: v_ for k_, v_ in zz_r.items() if k_ != "route"}, flush=True)
for e_ in EVENTS[-6:]:
    print({k_: (str(v_)[:140]) for k_, v_ in e_.items()}, flush=True)
print("state", state(), "kit", kit_mem(), flush=True)
