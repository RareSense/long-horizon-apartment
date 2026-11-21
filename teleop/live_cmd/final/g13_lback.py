# left hold a little back toward the body (less trunk tilt), as the skill's free1 ends (AI-operated)
PRE_ACTION("zz_left_back", {})
jaw_force["right"] = 20.0; jaw_target["right"] = 0.036
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.06, step=0.05)
    print("left to", zz_t, zz_r, "held L", cloth_held("left"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "knees", zz_knees(), "fell", fallen(), flush=True)
op.run(1.0)
print("fold target", bc_fold_target(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "inside", in_container(zz_BL, zz_hb()), flush=True)
P_ = zz_w().points(0); U_ = zz_uv(); hc_, hr_ = bc_wall(zz_hb()); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_])
o_ = np.flatnonzero(np.linalg.norm(P_[:, :2] - hc_, axis=1) > hr_ + 0.005)
for i_ in o_[np.argsort(-P_[o_, 2])][:14]:
    print("  outside high", int(i_), "rf", np.round(B_[i_], 3).tolist(), "uv", np.round(U_[i_], 2).tolist(), "r", round(float(np.linalg.norm(P_[i_, :2] - hc_)), 3), flush=True)
print("pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "tilt", round(pelvis_tilt(), 3), "pelvis", state()["pelvis"], flush=True)
cc_ = P_[o_[np.argmax(P_[o_, 2])]] if len(o_) else pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.6, 0.35, 0.3]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.7]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.4, 0.3]), cc_, "from the south-west")
print("look", zz_img(t_, "g13_lback"), flush=True)
