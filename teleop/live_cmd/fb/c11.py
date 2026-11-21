ck_load(os.path.join(RUN, "checkpoints", "0324_act_fb_two_hands_before_E_release"))
gait_on(); settle_after_load()
print("loaded: held L/R", cloth_held("left"), cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "pads L/R", np.round(pad_mid("left"), 3).tolist(), np.round(pad_mid("right"), 3).tolist(), flush=True)
zz_af = zz_release("right"); op.run(0.6)
print("E released: at_fingers R", zz_af, zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), flush=True)
for zz_t in ((0.42, -0.07, 1.32), (0.25, -0.12, 1.32), (0.18, -0.22, 1.15)):
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.08, step=0.05)
    print("right to", zz_t, zz_r, "at_fingers R", zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "tilt", round(pelvis_tilt(), 3), "touch", contact_report(), flush=True)
print("look", zz_look(np.array([-2.18, -1.82, 0.85]), "E_released2", dist=1.4, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
