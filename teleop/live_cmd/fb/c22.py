def zz_out():
    P_ = zz_w().points(0); hc_ = obj_rect(zz_hb()).c; U_ = zz_uv()
    o_ = np.linalg.norm(P_[:, :2] - hc_, axis=1) > 0.257
    return dict(n=int(o_.sum()), share=round(float(o_.mean()), 3), z_lo=round(float(P_[o_, 2].min()), 3) if o_.any() else None, below_rim_outside=int((o_ & (P_[:, 2] < 0.59)).sum()))
for zz_t in ZZ_TR:
    tw_ = zz_rf(zz_t) if zz_t[0] is not None else np.r_[pad_mid("right")[:2], zz_t[2]]
    zz_r = zz_pads_to("right", tw_, Q=None, speed=0.06, step=0.05)
    print("right to", zz_t, {k_: zz_r[k_] for k_ in ("err", "pad", "tilt")}, "held L/R", cloth_held("left"), cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), "outside", zz_out(), "touch", contact_report()["body"], "knees", [v_[0] for k_, v_ in zz_knees().items() if "knee" in k_], "fell", fallen(), flush=True)
print("pelvis", state()["pelvis"], "left pad", np.round(pad_mid("left"), 3).tolist(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), flush=True)
print("look", zz_look(np.array([-2.2, -1.8, 0.85]), "both_up", dist=1.4, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
