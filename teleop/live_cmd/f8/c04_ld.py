ck_load(os.path.join(RUN, "checkpoints", "0284_act_unlock_grip")); gait_on(); op.run(0.3)
R_ = ts.ee_pose("left")[1]
print("loaded", state(), "pad", np.round(pad_mid("left"), 3).tolist(), "finger axis x", np.round(R_[:, 0], 2).tolist(), "close axis y", np.round(R_[:, 1], 2).tolist(), "LOCK", list(LOCK), "HELD", list(HELD), flush=True)
print("stocking", in_container(zz_n, zz_cb), "box", [np.round(v_, 3).tolist() for v_ in garment_box(zz_n)], flush=True)
print(look_hand("left", "stock_over_basket"), flush=True)
