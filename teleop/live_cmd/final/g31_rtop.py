# right hand up out of the cloth, jaws turned to close ACROSS the body (fingers down), over the sagging far-end sheet south of the handle (AI-operated)
PRE_ACTION("zz_right_up_turn", {})
jaw_force["right"] = 20.0; jaw_target["right"] = JAW_OPEN
p_, y_ = base(); zz_fwd = RM.rz(y_)[:, 0]; zz_lat = RM.rz(y_)[:, 1]
a_ = np.radians(ZZ_TILT)
zz_QRL = {"right": q_(zz_R(np.sin(a_) * zz_fwd + np.cos(a_) * np.array([0, 0, -1.0]), zz_lat))}
hp_ = pad_mid("right")
zz_r = zz_pads_to("right", hp_ + np.array([0, 0, 0.09]), Q=zz_QRF, speed=0.05, step=0.04)
print("right up", zz_r, "at_f", zz_w().at_fingers("right"), "out", bc_out(zz_BL, zz_hb()), flush=True)
for zz_t in ZZ_TR:
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=zz_QRL, speed=0.05, step=0.04)
    Rn_ = ts.ee_pose("right")[1]; pa_, pb_ = pads("right"); Rb_ = RM.rz(base()[1])
    print("right to", zz_t, zz_r, "fingers rf", np.round(Rb_.T @ Rn_[:, 0], 2).tolist(), "close rf", np.round(Rb_.T @ Rn_[:, 1], 2).tolist(), "pads rf", np.round(zz_to_rf(pa_), 3).tolist(), np.round(zz_to_rf(pb_), 3).tolist(),
          "pad_low", round(pad_low("right"), 3), "caught", len(zz_w().caught("right")), "at_f", zz_w().at_fingers("right"), "held L", cloth_held("left"), "out", bc_out(zz_BL, zz_hb()), "touch", contact_report()["body"], "knees", zz_knees(), "fell", fallen(), flush=True)
def zz_under(sd, r=0.05):
    """Cloth under and around the pads: per sheet region the top height near the pad middle."""
    P_ = zz_w().points(0); U_ = zz_uv(); pm_ = pad_mid(sd)
    k_ = np.flatnonzero(np.linalg.norm(P_[:, :2] - pm_[:2], axis=1) < r)
    out_ = {}
    for nm_, s_ in (("far", U_[k_, 0] > 0.15), ("mid", np.abs(U_[k_, 0]) <= 0.15), ("first", U_[k_, 0] < -0.15)):
        if s_.any():
            zs_ = P_[k_[s_], 2]
            out_[nm_] = dict(n=int(s_.sum()), z_lo=round(float(zs_.min()), 3), z_hi=round(float(zs_.max()), 3), uv_mean=np.round(U_[k_[s_]].mean(0), 2).tolist())
    return out_
print("under the pads (5 cm):", zz_under("right"), "pad rf", np.round(zz_to_rf(pad_mid("right")), 3).tolist(), flush=True)
cc_ = pad_mid("right") - np.array([0, 0, 0.06])
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, -0.05, 0.1]), cc_, "from the west")
print("look", zz_img(t_, "g31_rtop"), flush=True)
