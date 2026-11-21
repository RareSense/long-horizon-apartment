print(floor_first(["r125i2_flat"])[:3], flush=True)
MON["trace"] = []; MON["t_max"] = 900.0
globals()["CARRY_JOINTS"] = True
try:
    zz_o = zz_pick_put("r125i2_flat", (1.16, -2.27))
finally:
    globals()["CARRY_JOINTS"] = False
print("OUT", str(zz_o)[:1500], flush=True)
print("state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
