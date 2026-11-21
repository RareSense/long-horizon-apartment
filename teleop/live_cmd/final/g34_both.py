# both holds together down into the opening, toward the hamper's middle (AI-operated)
print("ck", ck_save("g_both_up_before_lowering", kind="act"), "frame", rec.n, flush=True)
for zz_pr in ZZ_PAIRS:
    bc_both([zz_pr], speed=0.05)
    Rb_ = RM.rz(base()[1])
    print("both to", zz_pr, "pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "held L/R", cloth_held("left"), cloth_held("right"), "out", bc_out(zz_BL, zz_hb()), "inside", in_container(zz_BL, zz_hb()),
          "touch", contact_report()["body"], "knees", zz_knees(), "tilt", round(pelvis_tilt(), 3), "fell", fallen(), flush=True)
    if fallen():
        break
op.run(0.6)
for s_ in SIDES:
    a_, b_ = pads(s_); Rn_ = ts.ee_pose(s_)[1]
    print(s_, "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 1], 2).tolist(), "pads z", round(float(a_[2]), 3), round(float(b_[2]), 3), "pad r from centre", round(float(np.linalg.norm(pad_mid(s_)[:2] - obj_rect(zz_hb()).c)), 3), flush=True)
P_ = zz_w().points(0); hc_, hr_ = bc_wall(zz_hb()); rr_ = np.linalg.norm(P_[:, :2] - hc_, axis=1)
print("cloth r max", round(float(rr_.max()), 3), "share with r > 0.22:", round(float((rr_ > 0.22).mean()), 3), "their z lo/hi", (round(float(P_[rr_ > 0.22, 2].min()), 3), round(float(P_[rr_ > 0.22, 2].max()), 3)) if (rr_ > 0.22).any() else None, "lowest", round(float(P_[:, 2].min()), 3), "top", round(float(P_[:, 2].max()), 3), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print(n_, item_check(n_), flush=True)
print("look", zz_look(np.array([hc_[0], hc_[1], 0.75]), "g34_both", dist=1.3, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
