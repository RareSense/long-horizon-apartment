MON["trace"] = []
try:
    zz_r = go_item("r196i1_plastic_bag")
except RuntimeError as ex_:
    print("go_item err", str(ex_)[:300], "-> tight", flush=True)
    zz_r = with_tight(lambda: go_item("r196i1_plastic_bag"))
print("state", state(), "fell", fallen(), "touch", contact_report(), "kit", kit_mem(), flush=True)
