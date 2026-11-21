# reload before the left release (the open hand took cloth up with it) and look at how the cloth sits in the left jaws (AI-operated)
CK_RELOAD = os.path.join(CK_DIR, "1518_act_g_before_left_release_in")
print("frame before load", rec.n, flush=True)
ck_load(CK_RELOAD); gait_on(); op.run(0.3); sync_cloth(force=True)
print("RELOADED", CK_RELOAD, "frame", rec.n, flush=True)
print("held L/R", cloth_held("left"), cloth_held("right"), "LOCK", {s_: len(LOCK[s_][1]) for s_ in LOCK}, "HELD", HELD, "inside", in_container(zz_BL, zz_hb()), "out", bc_out(zz_BL, zz_hb()), "fell", fallen(), flush=True)
def zz_hand_cloth(sd, r=0.07):
    P_ = zz_w().points(0); U_ = zz_uv()
    a_, b_ = pads(sd); mid_ = (a_ + b_) / 2; ax_ = (b_ - a_); ax_ = ax_ / np.linalg.norm(ax_)
    Rn_ = ts.ee_pose(sd)[1]; f_ = Rn_[:, 0] - (Rn_[:, 0] @ ax_) * ax_; f_ = f_ / np.linalg.norm(f_); c_ = np.cross(ax_, f_)
    k_ = np.flatnonzero(np.linalg.norm(P_ - mid_, axis=1) < r)
    L_ = np.column_stack([(P_[k_] - mid_) @ ax_, (P_[k_] - mid_) @ f_, (P_[k_] - mid_) @ c_])
    print(sd, "cloth within", r, "of the pad middle: n", len(k_), "| closing axis world", np.round(ax_, 2).tolist(), "fingers world", np.round(f_, 2).tolist(), "across world", np.round(c_, 2).tolist(), flush=True)
    # raster: columns = along the closing axis (-7..7 cm), rows = along the fingers (tip side at the bottom); cell = count
    for fr_ in np.arange(-0.06, 0.061, 0.02):
        row_ = ""
        for al_ in np.arange(-0.07, 0.071, 0.02):
            s_ = (np.abs(L_[:, 0] - al_) < 0.01) & (np.abs(L_[:, 1] - fr_) < 0.01)
            row_ += (" %2d" % int(s_.sum())) if s_.any() else "  ."
        print("   along fingers %+.2f:" % fr_, row_, flush=True)
    print("   across range of those points", np.round([L_[:, 2].min(), L_[:, 2].max()], 3).tolist() if len(k_) else None, "(pads at closing axis -/+ %.3f)" % (float(np.linalg.norm(b_ - a_)) / 2), flush=True)
zz_hand_cloth("left")
a_, b_ = pads("left"); Rn_ = ts.ee_pose("left")[1]
print("left pad rf", np.round(zz_to_rf(pad_mid("left")), 3).tolist(), "fingers rf", np.round(RM.rz(base()[1]).T @ Rn_[:, 0], 2).tolist(), "gap", round(gap("left"), 4), "held uv", np.round(zz_uv()[LOCK["left"][1]], 2).tolist(), flush=True)
print("look hand", look_hand("left", "g38_left"), flush=True)
