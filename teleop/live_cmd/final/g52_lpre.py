# left hand, fingers DOWN (ZZ_TILT forward) and jaws closing fore-aft, beside the far sleeve strip (u > 0) hanging in the opening (AI-operated)
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
a_ = np.radians(ZZ_TILT)
zz_QLF = {"left": q_(zz_R(np.sin(a_) * zz_fwd + np.cos(a_) * np.array([0, 0, -1.0]), np.cos(a_) * zz_fwd + np.sin(a_) * np.array([0, 0, 1.0])))}
PRE_ACTION("zz_left_pre", {})
jaw_force["left"] = 20.0; jaw_target["left"] = JAW_OPEN; op.run(0.3)
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=zz_QLF, speed=0.08, step=ZZ_STEP)
    Rn_ = ts.ee_pose("left")[1]; pa_, pb_ = pads("left"); Rb_ = RM.rz(base()[1]); cg_ = zz_w().caught("left")
    print("left to", zz_t, zz_r, "fingers rf", np.round(Rb_.T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(Rb_.T @ Rn_[:, 1], 2).tolist(), "pads rf", np.round(zz_to_rf(pa_), 3).tolist(), np.round(zz_to_rf(pb_), 3).tolist(),
          "pad_low", round(pad_low("left"), 3), "caught", len(cg_), "uv", np.round(zz_uv()[cg_].mean(0), 2).tolist() if len(cg_) else None, "at_f", zz_w().at_fingers("left"), "held R", cloth_held("right"), "out", zz_out_parts()["share"],
          "touch", contact_report()["body"], contact_report()["body_who"], "knees", zz_knees(), "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0:
        break
P_ = zz_w().points(0); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); U_ = zz_uv(); pm_ = zz_to_rf(pad_mid("left"))
s_ = np.flatnonzero((np.abs(B_[:, 2] - pm_[2]) < 0.012) & (U_[:, 0] > 0.3))
if len(s_):
    print("far sleeve (u > 0.3) at the pad height: n", len(s_), "rf x", round(float(B_[s_, 0].min()), 3), round(float(B_[s_, 0].max()), 3), "y", round(float(B_[s_, 1].min()), 3), round(float(B_[s_, 1].max()), 3), "u", round(float(U_[s_, 0].min()), 2), round(float(U_[s_, 0].max()), 2), flush=True)
s_ = np.flatnonzero((np.abs(B_[:, 2] - pm_[2]) < 0.012) & (U_[:, 0] < -0.3))
if len(s_):
    print("near sleeve (u < -0.3) at the pad height: n", len(s_), "rf x", round(float(B_[s_, 0].min()), 3), round(float(B_[s_, 0].max()), 3), "y", round(float(B_[s_, 1].min()), 3), round(float(B_[s_, 1].max()), 3), "u", round(float(U_[s_, 0].min()), 2), round(float(U_[s_, 0].max()), 2), flush=True)
print("pad rf", np.round(pm_, 3).tolist(), "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), flush=True)
cc_ = pad_mid("left")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.55, 0.25, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([0.1, -0.6, 0.25]), cc_, "from the south")
print("look", zz_img(t_, "g52_lpre"), flush=True)
