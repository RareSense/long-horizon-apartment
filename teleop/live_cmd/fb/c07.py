for zz_k in range(ZZ_N):
    zz_r = zz_step_to(zz_o, zz_it, zz_QL, maxs=0.04)
    print("step", zz_k, {k_: zz_r[k_] for k_ in ("left", "in_pads", "caught", "caught_uv", "pad_rf", "tilt", "touch")}, "tgt", np.round(zz_w().points(0)[zz_it], 3).tolist(), "fell", fallen(), flush=True)
    if zz_r["left"] < 0.012 or fallen():
        break
cg_ = zz_w().caught(zz_o)
print("caught uv:", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, "knees", zz_knees(), flush=True)
cc_ = pad_mid(zz_o)
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([0.5, -0.4, 0.2]), cc_, "from the south-east")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([0.45, 0.45, 0.25]), cc_, "from the north-east")
print("look", zz_img(t_, "left_in"), flush=True)
