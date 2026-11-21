MON["held"] = {}; MON["on"] = False
ck_load(os.path.join(RUN, "checkpoints", "0284_act_unlock_grip")); gait_on(); op.run(0.3)
print("loaded", state(), "LOCK", list(LOCK), "stock", in_container(zz_n, zz_cb), flush=True)
