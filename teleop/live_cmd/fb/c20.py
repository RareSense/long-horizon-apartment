for zz_k in range(ZZ_N):
    zz_r = zz_step_to("right", ZZ_IT2, zz_QRT, maxs=0.025, speed=0.03, off=ZZ_OFF)
    cg_ = zz_w().caught("right")
    print("in", zz_k, {k_: zz_r[k_] for k_ in ("left", "in_pads", "caught", "caught_uv", "touch", "tilt")}, "pad", np.round(pad_mid("right"), 3).tolist(), "pad_low", round(pad_low("right"), 3), "tgt", np.round(zz_w().points(0)[ZZ_IT2], 3).tolist(), "who", contact_report()["body_who"], flush=True)
    if zz_r["left"] < 0.008 or zz_r["touch"] > 3.0 or fallen():
        break
cg_ = zz_w().caught("right")
print("between the pads uv:", np.round(zz_uv()[cg_], 2).tolist() if len(cg_) else None, "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "pad r from hamper", [round(float(np.linalg.norm(x_[:2] - obj_rect(zz_hb()).c)), 3) for x_ in pads("right")], flush=True)
cc_ = pad_mid("right")
t_ = [os.path.join(zz_LOOK_DIR, f"_c{i}.jpg") for i in range(3)]
close(t_[0], cc_ + np.array([-0.5, 0.3, 0.25]), cc_, "from the north-west")
close(t_[1], cc_ + np.array([0.03, 0.02, 0.6]), cc_, "from above")
close(t_[2], cc_ + np.array([-0.45, -0.35, 0.25]), cc_, "from the south-west")
print("look", zz_img(t_, "right_in2"), flush=True)
