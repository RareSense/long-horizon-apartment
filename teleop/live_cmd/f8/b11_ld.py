ck_load(os.path.join(RUN, "checkpoints", "0162_act__turn_on_spot")); gait_on(); op.run(0.3)
print("loaded", state(), "bin", [np.round(v_, 3).tolist() for v_ in obj_box(zz_bin)], "bag", np.round(centre(zz_b), 3).tolist(), "held", list(HELD), "grip", grip_check("left", None, min_gap=0.004).get("ok"), "touch", contact_report(), flush=True)
print(look3("bin_pre_turn"), flush=True)
