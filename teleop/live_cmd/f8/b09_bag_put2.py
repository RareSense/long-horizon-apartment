globals()["CARRY_JOINTS"] = True
try:
    zz_f = with_tight(lambda: finish_put("r196i1_plastic_bag", "left"))
finally:
    globals()["CARRY_JOINTS"] = False
print("PUT", str(zz_f)[:1500], flush=True)
print("bag", np.round(centre(zz_b), 3).tolist(), "state", state(), "fell", fallen(), "done", len(DONE), "kit", kit_mem(), flush=True)
