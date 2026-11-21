for zz_k in range(ZZ_N):
    PRE_ACTION("zz_hand_up", {})
    hp_ = ts.ee_pose("right")[0]
    op.move({"right": [hp_[0], hp_[1], hp_[2] + 0.04]}, speed=0.05, timeout=3.0, tol=0.008); op.run(0.4)
    print("up", zz_k, "pad", np.round(pad_mid("right"), 3).tolist(), "at_fingers", zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "top", round(float(zz_w().points(0)[:, 2].max()), 3), flush=True)
print("look", zz_look(np.array([-2.14, -1.85, 0.7]), "hand_up", dist=1.3, h=0.8, dirs=(20.0, 160.0), top=True), flush=True)
