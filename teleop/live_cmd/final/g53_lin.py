# left hand (fingers down, jaws fore-aft, open): small moves ZZ_MOVES (robot frame) toward the far sleeve strip (AI-operated)
def zz_sleeve_at(sd, far=True, dz=0.012):
    P_ = zz_w().points(0); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); U_ = zz_uv(); pm_ = zz_to_rf(pad_mid(sd))
    s_ = np.flatnonzero((np.abs(B_[:, 2] - pm_[2]) < dz) & ((U_[:, 0] > 0.3) if far else (U_[:, 0] < -0.3)))
    return [(int(i_), np.round(B_[i_] - pm_, 3).tolist(), np.round(U_[i_], 2).tolist()) for i_ in s_[np.argsort(-B_[s_, 1])]]
for zz_k, zz_mv in enumerate(ZZ_MOVES):
    PRE_ACTION("zz_left_in", dict(k=zz_k, d=list(zz_mv)))
    Rb_ = RM.rz(base()[1]); hp_ = ts.ee_pose("left")[0]
    op.move({"left": (hp_ + Rb_ @ np.asarray(zz_mv, float)).tolist()}, speed=0.04, quats=zz_QLF, timeout=3.0, tol=0.006); op.run(0.3)
    cg_ = zz_w().caught("left"); pa_, pb_ = pads("left"); mid_ = (pa_ + pb_) / 2; ax_ = (pb_ - pa_) / np.linalg.norm(pb_ - pa_)
    print("move", zz_k, list(zz_mv), "pad rf", np.round(zz_to_rf(pad_mid("left")), 3).tolist(), "pads x", round(float(zz_to_rf(pa_)[0]), 3), round(float(zz_to_rf(pb_)[0]), 3), "pad_low", round(pad_low("left"), 3), "caught", len(cg_),
          "along", np.round((zz_w().points(0)[cg_] - mid_) @ ax_, 3).tolist() if len(cg_) else None, "u", np.round(zz_uv()[cg_, 0], 2).tolist() if len(cg_) else None, "at_f", zz_w().at_fingers("left"), "out", zz_out_parts()["share"],
          "touch", contact_report()["body"], contact_report()["body_who"], "held R", cloth_held("right"), "fell", fallen(), flush=True)
    if fallen() or contact_report()["body"] > 3.0:
        break
print("far sleeve at the pad height (rel pad: ahead, left, up):", zz_sleeve_at("left", True), flush=True)
print("near sleeve at the pad height:", zz_sleeve_at("left", False)[:10], flush=True)
print("tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "pelvis", state()["pelvis"], flush=True)
cc_ = pad_mid("left")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.55, 0.25, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([0.1, -0.6, 0.25]), cc_, "from the south")
print("look", zz_img(t_, "g53_lin"), flush=True)
