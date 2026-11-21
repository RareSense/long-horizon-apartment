# right hand (fingers down-forward, jaws across the body, open) down onto the sagging sheet in small moves (AI-operated)
for zz_k in range(ZZ_N):
    PRE_ACTION("zz_right_down", dict(k=zz_k))
    Rb_ = RM.rz(base()[1]); hp_ = ts.ee_pose("right")[0]
    op.move({"right": (hp_ + Rb_ @ np.asarray(ZZ_D, float)).tolist()}, speed=0.03, quats=zz_QRL, timeout=3.0, tol=0.005); op.run(0.3)
    cg_ = zz_w().caught("right"); U_ = zz_uv()
    print("down", zz_k, "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pad_low", round(pad_low("right"), 3), "caught", len(cg_), "far", int((U_[cg_, 0] > 0.15).sum()) if len(cg_) else 0, "first", int((U_[cg_, 0] < -0.15).sum()) if len(cg_) else 0,
          "uv", np.round(U_[cg_], 2).tolist() if len(cg_) else None, "at_f", zz_w().at_fingers("right"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0 or pad_low("right") < ZZ_ZMIN:
        break
print("under the pads (5 cm):", zz_under("right"), "held L", cloth_held("left"), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
a_, b_ = pads("right"); hc_ = obj_rect(zz_hb()).c
print("pads world", np.round(a_, 3).tolist(), np.round(b_, 3).tolist(), "pad r from hamper centre", [round(float(np.linalg.norm(x_[:2] - hc_)), 3) for x_ in (a_, b_)], "handle bar: y -1.712, x -2.212..-2.088, top z 0.67", flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g32_rdown"), flush=True)
