HELD["left"] = {k: v for k, v in grip_check("left", None, min_gap=0.004).items()}
stand_with("left", (), T=2.5)
print("stood", state(), "bag", np.round(centre(zz_b), 3).tolist(), "grip", grip_check("left", None, min_gap=0.004).get("ok"), flush=True)
globals()["CARRY_JOINTS"] = True
try:
    zz_f = finish_put("r196i1_plastic_bag", "left")
finally:
    globals()["CARRY_JOINTS"] = False
print("PUT", str(zz_f)[:1500], flush=True)
print("bag", np.round(centre(zz_b), 3).tolist(), "state", state(), "fell", fallen(), "done", len(DONE), flush=True)
