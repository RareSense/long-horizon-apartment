# the jaws were closing on the hamper's north HANDLE bar (top z 0.67) under the cloth: open, raise the pads above it, centre on the cloth, squeeze (AI-operated)
PRE_ACTION("zz_right_above_handle", {})
jaw_force["right"] = 20.0; jaw_target["right"] = JAW_OPEN; op.run(0.6)
Rb_ = RM.rz(base()[1])
hp_ = ts.ee_pose("right")[0]
op.move({"right": (hp_ + Rb_ @ np.asarray(ZZ_D, float)).tolist()}, speed=0.03, quats=zz_QRF, timeout=3.0, tol=0.004); op.run(0.4)
def zz_along(sd):
    cg_ = zz_w().caught(sd)
    a_, b_ = pads(sd); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_) / np.linalg.norm(b_ - a_)
    al_ = (zz_w().points(0)[cg_] - mid_) @ ax_ if len(cg_) else np.zeros(0)
    return cg_, al_, ax_
for zz_k in range(3):
    cg_, al_, ax_ = zz_along("right")
    print("pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), "pad_low", round(pad_low("right"), 3), "gap", round(gap("right"), 4), "caught", len(cg_), "along", np.round(al_, 3).tolist(), "uv", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, flush=True)
    if not len(cg_) or abs(float(np.median(al_))) < 0.006:
        break
    sh_ = float(np.clip(np.median(al_), -0.02, 0.02))
    hp_ = ts.ee_pose("right")[0]
    op.move({"right": (hp_ + sh_ * ax_).tolist()}, speed=0.03, quats=zz_QRF, timeout=3.0, tol=0.004); op.run(0.4)
print("touch", contact_report(), "held L", cloth_held("left"), "out", bc_out(zz_BL, zz_hb()), "fell", fallen(), flush=True)
P_ = zz_w().points(0); B_ = np.array([zz_to_rf(q_xyz) for q_xyz in P_]); U_ = zz_uv(); pm_ = zz_to_rf(pad_mid("right"))
s_ = np.flatnonzero((np.abs(B_[:, 2] - pm_[2]) < 0.015) & (np.abs(B_[:, 0] - pm_[0]) < 0.08) & (np.abs(B_[:, 1] - pm_[1]) < 0.03))
for i_ in s_[np.argsort(B_[s_, 0])]:
    print("   cloth at the pad height:", int(i_), "rel pad (ahead, left, up)", np.round(B_[i_] - pm_, 3).tolist(), "uv", np.round(U_[i_], 2).tolist(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g26_above"), flush=True)
