zz_n = "r116i1_coat_pile"; zz_h = laundry_body()
jaw_target["right"] = 0.0
print("right pad rf", np.round(bc_to_rf(pad_mid("right")), 3).tolist(), flush=True)
zz_p = pad_mid("right")
bc_pads_to("right", np.r_[zz_p[:2], max(1.0, float(zz_p[2]) + 0.15)], speed=0.06, step=0.05)
bc_path("right", [(0.26, -0.20, 1.10), (0.16, -0.26, 0.95)], speed=0.08, step=0.05)
print("right away: inside", in_container(zz_n, zz_h), "out", bc_out(zz_n, zz_h), "at fingers R", bc_w(zz_n).at_fingers("right"), flush=True)
BC["stage"] = "both_up"
zz_r = bigcloth_into(zz_n, s1="right", start="lower_release", stop_after="retract")
for r_ in zz_r: print("RESULT", r_, flush=True)
print("inside", in_container(zz_n, zz_h), "out", bc_out(zz_n, zz_h), "state", state(), "touch", contact_report(), "LOCK", list(LOCK), "HELD", HELD, flush=True)
for n_ in GARMENTS: print(n_, in_container(n_, zz_h), flush=True)
