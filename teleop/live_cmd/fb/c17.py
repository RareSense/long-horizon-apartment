ZZ_MAXS = globals().get("ZZ_MAXS", 0.04)
zz_it2 = ZZ_IT2
for zz_k in range(ZZ_N):
    P_ = zz_w().points(0)
    if pad_mid("right")[2] - P_[zz_it2][2] < ZZ_STOP:
        break
    zz_r = zz_step_to("right", zz_it2, zz_QRD, maxs=ZZ_MAXS, speed=0.03, off=(0.0, 0.0, ZZ_STOP - 0.002))
    cg_ = zz_w().caught("right")
    print("down", zz_k, {k_: zz_r[k_] for k_ in ("left", "in_pads", "caught", "caught_uv", "touch", "tilt")}, "pad", np.round(pad_mid("right"), 3).tolist(), "pad_low", round(pad_low("right"), 3), "tgt", np.round(zz_w().points(0)[zz_it2], 3).tolist(),
          "knees", [v_[0] for k_, v_ in zz_knees().items() if "knee" in k_], "who", contact_report()["body_who"], flush=True)
    if zz_r["touch"] > 3.0 or fallen():
        break
cg_ = zz_w().caught("right")
print("between the pads uv:", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.45, -0.35, 0.25]), cc_, "from the south-west")
print("look", zz_img(t_, "right_down2"), flush=True)
