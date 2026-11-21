# run bigcloth stages ZZ_START..ZZ_STOP after the teleop left hold (AI-operated)
print("ck", ck_save("g_before_" + ZZ_START, kind="act"), "frame", rec.n, flush=True)
zz_r = bigcloth_into(zz_BL, s1="right", start=ZZ_START, stop_after=ZZ_STOP)
for r_ in zz_r:
    print("RESULT", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:260]) for k_, v_ in r_.items() if k_ != "look"}, flush=True)
    print("  stage look", r_.get("look"), flush=True)
print("held L/R", cloth_held("left"), cloth_held("right"), "LOCK", {s_: len(LOCK[s_][1]) for s_ in LOCK}, "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), flush=True)
print("pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "state", state(), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "fell", fallen(), flush=True)
P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb())
o_ = np.linalg.norm(P_[:, :2] - hc_, axis=1) > hr_
if o_.any():
    B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_[o_]])
    print("outside n", int(o_.sum()), "uv lo/hi", np.round(U_[o_].min(0), 2).tolist(), np.round(U_[o_].max(0), 2).tolist(), "z lo/hi", round(float(P_[o_, 2].min()), 3), round(float(P_[o_, 2].max()), 3), "rf lo/hi", np.round(B_.min(0), 3).tolist(), np.round(B_.max(0), 3).tolist(), flush=True)
for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket"):
    print(n_, item_check(n_), flush=True)
print("look", zz_look(np.array([hc_[0], hc_[1], 0.85]), "g07_" + ZZ_STOP, dist=1.4, h=0.6, dirs=(0.0, 180.0, 270.0), top=True), flush=True)
