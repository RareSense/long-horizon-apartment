PRE_ACTION("zz_left_lower", {})
for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.05, step=0.05)
    print("left to", zz_t, {k_: zz_r[k_] for k_ in ("err", "pad", "tilt")}, "held L", cloth_held("left"), "blanket", in_container(zz_BL, zz_hb()), "outside", zz_out(), "touch", contact_report()["body"], "knees", [v_[0] for k_, v_ in zz_knees().items() if "knee" in k_], "fell", fallen(), flush=True)
Rn_ = ts.ee_pose("left")[1]
print("left fingers dir", np.round(Rn_[:, 0], 2).tolist(), "close dir", np.round(Rn_[:, 1], 2).tolist(), "top z", round(float(zz_w().points(0)[:, 2].max()), 3), flush=True)
print("look", zz_look(np.array([-2.2, -1.85, 0.75]), "left_lower", dist=1.3, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
