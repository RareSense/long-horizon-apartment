exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
rest_hands(SIDES); op.run(1.0)
print("START", ck_save("shoe1_placed_test", kind="start"), flush=True)
ZR = shoe_to_mat("r105i2_shoe", record=False)
print("RESULT", ZR, flush=True)
print(close(os.path.join(LK, "s10_mat_above.jpg"), np.r_[1.66, -1.98, 1.5], np.r_[1.72, -2.05, 0.0], "mat from above"), flush=True)
