# right hold (far end + first end edge) up and over the opening: the corner outside comes over the rim (AI-operated)
print("ck", ck_save("g_both_held_before_right_lift", kind="act"), "frame", rec.n, flush=True)
for zz_t in ZZ_TR:
    PRE_ACTION("zz_right_lift", dict(to=list(zz_t)))
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.05, step=0.04)
    print("right to", zz_t, zz_r, "held L/R", cloth_held("left"), cloth_held("right"), "out", bc_out(zz_BL, zz_hb()), "inside", in_container(zz_BL, zz_hb()), "touch", contact_report()["body"], "knees", zz_knees(), "fell", fallen(), flush=True)
    if fallen() or not cloth_held("right"):
        break
op.run(0.8)
P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb()); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); rr_ = np.linalg.norm(P_[:, :2] - hc_, axis=1)
o_ = rr_ > hr_
print("outside n", int(o_.sum()), "uv lo/hi", (np.round(U_[o_].min(0), 2).tolist(), np.round(U_[o_].max(0), 2).tolist()) if o_.any() else None, "z lo/hi", (round(float(P_[o_, 2].min()), 3), round(float(P_[o_, 2].max()), 3)) if o_.any() else None, flush=True)
for uv_ in ((0.5, -0.375), (0.5, -0.2), (0.4, -0.375), (0.5, 0.0), (0.5, 0.375)):
    i_ = int(np.argmin(np.linalg.norm(U_ - np.array(uv_), axis=1)))
    print("uv", uv_, "rf", np.round(B_[i_], 3).tolist(), "r", round(float(rr_[i_]), 3), flush=True)
print("pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "tilt", round(pelvis_tilt(), 3), "pelvis", state()["pelvis"], "hamper", np.round(hc_, 3).tolist(), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print(n_, item_check(n_), flush=True)
print("look", zz_look(np.array([hc_[0], hc_[1], 0.8]), "g33_rlift", dist=1.3, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
