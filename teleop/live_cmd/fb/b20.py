for zz_t in ZZ_TARGETS:
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.08, step=0.06)
    P_ = zz_w().points(0)
    print("to", zz_t, zz_r, "pad", np.round(pad_mid("right"), 3).tolist(), "pelvis", state()["pelvis"], "blanket", in_container(zz_BL, zz_hb()), "touch", contact_report(), "fell", fallen(), flush=True)
print("hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "held", cloth_held("right"), flush=True)
print("look", zz_look(np.array([-2.14, -1.85, 0.75]), "reach", dist=1.5, h=0.8, dirs=(20.0, 160.0), top=True), flush=True)
