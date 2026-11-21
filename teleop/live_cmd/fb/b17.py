PRE_ACTION("zz_raise_high", {})
for zz_t in ((0.34, -0.13, 1.10), (0.34, -0.13, 1.22), (0.34, -0.13, 1.30)):
    zz_r = zz_pads_to("right", zz_rf(zz_t), Q=None, speed=0.12)
    print("to", zz_t, zz_r, "lowest", round(float(zz_w().points(0)[:, 2].min()), 3), "pelvis", state()["pelvis"], "fell", fallen(), contact_report(), flush=True)
op.run(1.5)
print("hang", zz_hang("right"), "held", cloth_held("right"), "blanket box", [np.round(v_, 3).tolist() for v_ in garment_box(zz_BL)], flush=True)
print("look", zz_look(np.array([-2.14, -1.75, 0.7]), "raised_at_pre", dist=1.7, h=0.8, dirs=(20.0, 160.0), top=False), flush=True)
