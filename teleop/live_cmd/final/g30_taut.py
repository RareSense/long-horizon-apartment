# slack sheet lies flat beside the fingers: open, left hold back up (sheet taut and steep above the handle), then centre the right pads on it above the handle (AI-operated)
PRE_ACTION("zz_right_reopen5", {})
jaw_force["right"] = 20.0
for jv_ in (0.012, 0.025, JAW_OPEN):
    jaw_target["right"] = jv_; op.run(0.3)
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.05, step=0.04)
    print("left to", zz_t, zz_r, "held L", cloth_held("left"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "fell", fallen(), flush=True)
op.run(0.8)
def zz_along(sd):
    cg_ = zz_w().caught(sd)
    a_, b_ = pads(sd); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_) / np.linalg.norm(b_ - a_)
    al_ = (zz_w().points(0)[cg_] - mid_) @ ax_ if len(cg_) else np.zeros(0)
    return cg_, al_, ax_
def zz_near_pad():
    P_ = zz_w().points(0); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); U_ = zz_uv(); pm_ = zz_to_rf(pad_mid("right"))
    s_ = np.flatnonzero((np.abs(B_[:, 2] - pm_[2]) < 0.012) & (np.abs(B_[:, 0] - pm_[0]) < 0.07) & (np.abs(B_[:, 1] - pm_[1]) < 0.05))
    for i_ in s_[np.argsort(B_[s_, 1])]:
        print("   cloth at the pad height:", int(i_), "rel pad (ahead, left, up)", np.round(B_[i_] - pm_, 3).tolist(), "uv", np.round(U_[i_], 2).tolist(), flush=True)
cg_, al_, ax_ = zz_along("right")
print("pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pad_low", round(pad_low("right"), 3), "gap", round(gap("right"), 4), "caught", len(cg_), "along", np.round(al_, 3).tolist(), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
zz_near_pad()
print("pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g30_taut"), flush=True)
