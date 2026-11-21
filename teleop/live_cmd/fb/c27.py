print("ck", ck_save("fb_blanket_inside_left_still_holding", kind="act"), flush=True)
zz_af = zz_release("left"); op.run(1.0)
print("S1 released: at_fingers L", zz_af, zz_w().at_fingers("left"), "blanket", in_container(zz_BL, zz_hb()), "LOCK", dict(LOCK), "HELD", dict(HELD), flush=True)
for zz_k in range(4):
    PRE_ACTION("zz_left_up", {})
    hp_ = ts.ee_pose("left")[0]
    op.move({"left": [hp_[0], hp_[1], hp_[2] + 0.04]}, speed=0.05, timeout=3.0, tol=0.008); op.run(0.4)
    print("up", zz_k, "pad", np.round(pad_mid("left"), 3).tolist(), "at_fingers L", zz_w().at_fingers("left"), "blanket", in_container(zz_BL, zz_hb()), "top", round(float(zz_w().points(0)[:, 2].max()), 3), "touch", contact_report()["body"], flush=True)
print("look", zz_look(np.array([-2.2, -1.85, 0.7]), "S1_released", dist=1.3, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
