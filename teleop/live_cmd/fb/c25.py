ZZ_BOTH = [((0.52, 0.00, 1.14), (0.48, -0.10, 1.06))]
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\c23.py", encoding="utf-8").read())
print("ck", ck_save("fb_both_hands_before_S2_release", kind="act"), flush=True)
zz_af = zz_release("right"); op.run(0.6)
print("S2 released: at_fingers R", zz_af, zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "outside", zz_out(), flush=True)
for zz_t in ((0.46, -0.12, 1.16), (0.26, -0.20, 1.16), (0.16, -0.26, 0.95)):
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.08, step=0.05)
    print("right to", zz_t, {k_: zz_r[k_] for k_ in ("err", "pad", "tilt")}, "at_fingers R", zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "outside", zz_out(), "touch", contact_report()["body"], flush=True)
op.run(1.5)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\c24.py", encoding="utf-8").read())
print("held L", cloth_held("left"), "hang L", zz_hang("left"), "knees", [v_[0] for k_, v_ in zz_knees().items() if "knee" in k_], "tilt", round(pelvis_tilt(), 3), flush=True)
print("look", zz_look(np.array([-2.2, -1.8, 0.8]), "S2_released", dist=1.3, h=0.7, dirs=(20.0, 160.0, 90.0), top=True), flush=True)
