print(floor_first(["r120i2_duck"])[:2], flush=True)
MON["trace"] = []
try:
    zz_r = go_item("r120i2_duck")
except RuntimeError as ex_:
    print("err", str(ex_)[:200], "-> tight", flush=True)
    zz_r = with_tight(lambda: go_item("r120i2_duck"))
print("duck", np.round(centre(body_of("r120i2_duck")), 3).tolist(), "in basket", inside(body_of("r120i2_duck"), body_of("r186i1_basket")), "state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
