# left jaws (open, side by side, fingers ahead) onto the near fold of the strand in small moves (AI-operated)
zz_it = globals().get("ZZ_IT", 1121)
zz_off = ZZ_AHEAD * zz_fwd
for zz_k in range(ZZ_N):
    zz_r = zz_step_to(zz_o, zz_it, zz_QF, maxs=0.025, speed=0.04, off=zz_off)
    a_, b_ = pads(zz_o)
    print("step", zz_k, {k_: zz_r[k_] for k_ in ("left", "in_pads", "caught", "caught_uv", "pad_rf", "tilt", "touch")}, "tgt rf", np.round(zz_to_rf(zz_w().points(0)[zz_it]), 3).tolist(), "pads rf", np.round(zz_to_rf(a_), 3).tolist(), np.round(zz_to_rf(b_), 3).tolist(), "fell", fallen(), flush=True)
    if zz_r["left"] < 0.008 or fallen() or zz_r["touch"] > 3.0:
        break
cg_ = zz_w().caught(zz_o)
print("caught uv:", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, "knees", zz_knees(), "right held", cloth_held("right"), "blanket", in_container(zz_BL, zz_hb()), flush=True)
cc_ = pad_mid(zz_o)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.5, 0.2, 0.2]), cc_, "from the east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.55]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.5, 0.2, 0.2]), cc_, "from the west")
print("look", zz_img(t_, "g04_in"), flush=True)
