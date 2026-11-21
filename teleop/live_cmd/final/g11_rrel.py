# right hand lets its end go (fingers down-forward, jaws side by side), then draws back along the fingers (AI-operated)
print("ck", ck_save("g_before_right_release", kind="act"), "frame", rec.n, flush=True)
zz_af = zz_release("right"); op.run(0.8)
print("released: at_fingers R", zz_af, zz_w().at_fingers("right"), "caught R", len(zz_w().caught("right")), "held L", cloth_held("left"), "LOCK", list(LOCK), "HELD", HELD, "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), flush=True)
Rn_ = ts.ee_pose("right")[1]; f_ = Rn_[:, 0].copy()
for zz_k in range(ZZ_NB):
    PRE_ACTION("zz_right_back", dict(k=zz_k))
    hp_ = ts.ee_pose("right")[0]
    op.move({"right": (hp_ - 0.03 * f_).tolist()}, speed=0.04, quats=zz_QRT, timeout=3.0, tol=0.008); op.run(0.3)
    print("back", zz_k, "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "at_f R", zz_w().at_fingers("right"), "out", bc_out(zz_BL, zz_hb()), "top", round(float(zz_w().points(0)[:, 2].max()), 3), "touch", contact_report()["body"], "fell", fallen(), flush=True)
    if fallen():
        break
print("held L", cloth_held("left"), "pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.45, 0.25, 0.15]), cc_, "from the east")
close(t_[1], cc_ + np.array([-0.45, 0.25, 0.15]), cc_, "from the west")
close(t_[2], cc_ + np.array([-0.05, -0.5, 0.2]), cc_, "from the south")
print("look", zz_img(t_, "g11_rrel"), flush=True)
