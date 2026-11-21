# left hold down to release height with steep fingers, then let go: open, wait, hand straight up in small moves (AI-operated)
ZZ_TILT = 24.0
ZZ_TL = [(0.46, 0.0, 0.84), (0.46, 0.0, 0.76)]
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\g39_lvert.py", encoding="utf-8").read())
a_, b_ = pads("left")
print("ck", ck_save("g_before_left_release_steep", kind="act"), "frame", rec.n, "pads z", round(float(a_[2]), 3), round(float(b_[2]), 3), flush=True)
zz_af = zz_release("left"); op.run(1.2)
print("released left: at_fingers", zz_af, zz_w().at_fingers("left"), "caught", len(zz_w().caught("left")), "LOCK", list(LOCK), "HELD", HELD, "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "top", round(float(zz_w().points(0)[:, 2].max()), 3), flush=True)
for zz_k in range(ZZ_NB):
    PRE_ACTION("zz_hand_up", dict(side="left", k=zz_k))
    hp_ = ts.ee_pose("left")[0]
    op.move({"left": (hp_ + np.array([0, 0, 0.03])).tolist()}, speed=0.04, quats=zz_QLV, timeout=3.0, tol=0.008); op.run(0.3)
    P_ = zz_w().points(0)
    print("up", zz_k, "pad rf", np.round(zz_to_rf(pad_mid("left")), 3).tolist(), "at_f", zz_w().at_fingers("left"), "out", bc_out(zz_BL, zz_hb()), "top", round(float(P_[:, 2].max()), 3), "inside", in_container(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
    if fallen() or (zz_k >= 1 and zz_w().at_fingers("left") > 0 and P_[:, 2].max() > pad_low("left") - 0.02):
        print("cloth is coming up with the hand: stop", flush=True)
        break
hc_ = obj_rect(zz_hb()).c
print("look", zz_look(np.array([hc_[0], hc_[1], 0.7]), "g40_lrel", dist=1.3, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
