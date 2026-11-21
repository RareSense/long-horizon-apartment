PRE_ACTION("zz_both_seq", {})
for zz_tl, zz_tr in ZZ_BOTH:
    PRE_ACTION("zz_both_hands", dict(l=zz_tl, r=zz_tr))
    for k_ in range(6):
        el_ = zz_rf(zz_tl) - pad_mid("left"); er_ = zz_rf(zz_tr) - pad_mid("right")
        if max(np.linalg.norm(el_), np.linalg.norm(er_)) < 0.008:
            break
        ml_ = el_ if np.linalg.norm(el_) < 0.05 else el_ * 0.05 / np.linalg.norm(el_)
        mr_ = er_ if np.linalg.norm(er_) < 0.05 else er_ * 0.05 / np.linalg.norm(er_)
        op.move({"left": (ts.ee_pose("left")[0] + ml_).tolist(), "right": (ts.ee_pose("right")[0] + mr_).tolist()}, speed=0.05, timeout=4.0, tol=0.008); op.run(0.2)
    print("both to", zz_tl, zz_tr, "pads L", np.round(pad_mid("left"), 3).tolist(), "R", np.round(pad_mid("right"), 3).tolist(), "held", cloth_held("left"), cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), "outside", zz_out(),
          "touch", contact_report()["body"], "tilt", round(pelvis_tilt(), 3), "knees", [v_[0] for k_, v_ in zz_knees().items() if "knee" in k_], "fell", fallen(), flush=True)
print("pelvis", state()["pelvis"], "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), flush=True)
print("look", zz_look(np.array([-2.2, -1.85, 0.8]), "both_lower", dist=1.3, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
