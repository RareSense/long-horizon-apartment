print("ck", ck_save("fb_two_hands_before_E_release", kind="act"), flush=True)
zz_af = zz_release("right"); op.run(0.8)
print("E released: at_fingers R", zz_af, zz_w().at_fingers("right"), "held L", cloth_held("left"), "blanket", in_container(zz_BL, zz_hb()), flush=True)
p_, y_ = base(); zz_lat = RM.rz(y_)[:, 1]
zz_QRD = {"right": q_(R_down(zz_lat))}
for zz_t in ((0.36, -0.16, 1.05), (0.30, -0.18, 0.90)):
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=zz_QRD, speed=0.08, step=0.06)
    print("right to", zz_t, zz_r, "at_fingers R", zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "tilt", round(pelvis_tilt(), 3), "touch", contact_report(), flush=True)
op.run(1.0)
print("pelvis", state()["pelvis"], "knees", {k_: v_[0] for k_, v_ in zz_knees().items() if "knee" in k_}, "left pad", np.round(pad_mid("left"), 3).tolist(), "hang L", zz_hang("left"), flush=True)
print("look", zz_look(np.array([-2.18, -1.82, 0.85]), "E_released", dist=1.4, h=0.7, dirs=(20.0, 160.0), top=True), flush=True)
