# hand ZZ_S lets go inside the opening (jaws side by side, fingers down-forward) and draws back up along its fingers (AI-operated)
zz_s = ZZ_S
a_, b_ = pads(zz_s)
print("ck", ck_save(f"g_before_{zz_s}_release_in", kind="act"), "frame", rec.n, "pads z", round(float(a_[2]), 3), round(float(b_[2]), 3), flush=True)
zz_af = zz_release(zz_s); op.run(0.8)
print("released", zz_s, ": at_fingers", zz_af, zz_w().at_fingers(zz_s), "caught", len(zz_w().caught(zz_s)), "LOCK", list(LOCK), "HELD", HELD, "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), flush=True)
Rn_ = ts.ee_pose(zz_s)[1]; f_ = Rn_[:, 0].copy(); zz_Qk = {zz_s: q_(Rn_)}
dir_ = -f_ + np.array([0, 0, ZZ_UPB]); dir_ = dir_ / np.linalg.norm(dir_)
for zz_k in range(ZZ_NB):
    PRE_ACTION("zz_hand_back", dict(side=zz_s, k=zz_k))
    hp_ = ts.ee_pose(zz_s)[0]
    op.move({zz_s: (hp_ + 0.03 * dir_).tolist()}, speed=0.04, quats=zz_Qk, timeout=3.0, tol=0.008); op.run(0.3)
    P_ = zz_w().points(0)
    print("back", zz_k, "pad rf", np.round(zz_to_rf(pad_mid(zz_s)), 3).tolist(), "at_f", zz_w().at_fingers(zz_s), "out", bc_out(zz_BL, zz_hb()), "top", round(float(P_[:, 2].max()), 3), "inside", in_container(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
    if fallen():
        break
print("held L/R", cloth_held("left"), cloth_held("right"), "pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
hc_ = obj_rect(zz_hb()).c
print("look", zz_look(np.array([hc_[0], hc_[1], 0.7]), "g35_rel_" + zz_s, dist=1.3, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
