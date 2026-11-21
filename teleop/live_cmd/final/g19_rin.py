# right hand (fingers down, jaws fore-aft, open) sideways onto the far-end sheet at the rim in small moves (AI-operated)
zz_it2 = ZZ_IT2
for zz_k in range(ZZ_N):
    Rb_ = RM.rz(base()[1])
    e_ = Rb_.T @ (zz_w().points(0)[zz_it2] + np.array([0, 0, ZZ_DZ]) - pad_mid("right"))      # target - pad, robot frame
    if abs(e_[1]) < 0.008 and abs(e_[2]) < 0.008 and abs(e_[0]) < 0.008:
        break
    mv_ = np.array([np.clip(e_[0], -0.01, 0.01), np.clip(e_[1], -ZZ_MAXS, ZZ_MAXS), np.clip(e_[2], -0.03, 0.03)])
    PRE_ACTION("zz_right_in", dict(k=zz_k, d=np.round(mv_, 3).tolist()))
    hp_ = ts.ee_pose("right")[0]
    op.move({"right": (hp_ + Rb_ @ mv_).tolist()}, speed=0.04, quats=zz_QRF, timeout=3.0, tol=0.006); op.run(0.3)
    cg_ = zz_w().caught("right"); pa_, pb_ = pads("right")
    print("in", zz_k, "moved", np.round(mv_, 3).tolist(), "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pads x", round(float(zz_to_rf(pa_)[0]), 3), round(float(zz_to_rf(pb_)[0]), 3), "pad_low", round(pad_low("right"), 3),
          "tgt rf", np.round(zz_to_rf(zz_w().points(0)[zz_it2]), 3).tolist(), "in_pads", zz_in_pads("right", zz_it2), "caught", len(cg_), "uv", np.round(zz_uv()[cg_].mean(0), 2).tolist() if len(cg_) else None,
          "first end 39 in_pads", zz_in_pads("right", 39)[0], "touch", contact_report()["body"], contact_report()["body_who"], "out", bc_out(zz_BL, zz_hb())["share"], "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0:
        break
cg_ = zz_w().caught("right")
print("between the pads uv:", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
print("hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "held L", cloth_held("left"), "inside", in_container(zz_BL, zz_hb()), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g19_rin"), flush=True)
