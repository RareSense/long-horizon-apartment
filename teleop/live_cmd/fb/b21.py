ZZ_TARGETS = [(0.58, -0.05, 0.80)]
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\b20.py", encoding="utf-8").read())
print("ck", ck_save("fb_E_low_in_hamper_before_release", kind="act"), flush=True)
zz_af = zz_release("right")
op.run(1.0)
print("released: at_fingers", zz_af, zz_w().at_fingers("right"), "blanket", in_container(zz_BL, zz_hb()), "jaw", round(jaw("right"), 4), flush=True)
print("look", zz_look(np.array([-2.14, -1.85, 0.7]), "released_E", dist=1.3, h=0.8, dirs=(20.0, 160.0), top=True), flush=True)
