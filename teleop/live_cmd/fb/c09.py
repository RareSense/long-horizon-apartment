for zz_t in ZZ_TL:
    zz_r = zz_pads_to("left", zz_rf(zz_t), Q=None, speed=0.06, step=0.05)
    print("left to", zz_t, zz_r, "pad", np.round(pad_mid("left"), 3).tolist(), "held L/R", cloth_held("left"), cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), "touch", contact_report(), "knees", {k_: v_[0] for k_, v_ in zz_knees().items() if "knee" in k_}, "fell", fallen(), flush=True)
print("pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "right pad", np.round(pad_mid("right"), 3).tolist(), flush=True)
print("look", zz_look(np.array([-2.18, -1.82, 0.85]), "two_hands", dist=1.4, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
