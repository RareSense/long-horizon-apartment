ck_load(os.path.join(RUN, "checkpoints", "0512_item_r125i2_flat")); gait_on(); settle_after_load()
print("loaded", state(), "croc", np.round(centre(body_of("r122i1_croc")), 3).tolist(), flush=True)
mon_start(target=None)
try:
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, tag="off_mat")
        print("back", r_["at"], r_["yaw_deg"], "touch", r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "croc", np.round(centre(body_of("r122i1_croc")), 3).tolist(), "flat", np.round(centre(body_of("r125i2_flat")), 3).tolist(), flush=True)
