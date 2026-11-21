zz_it = 1223
for zz_k in range(ZZ_N):
    P_ = zz_w().points(0)
    if pad_mid("right")[2] - P_[zz_it][2] < 0.006:
        break
    zz_r = zz_step_to("right", zz_it, zz_QR, maxs=ZZ_STEP, speed=0.04)
    hc_ = obj_rect(zz_hb()).c
    print("down", zz_k, {k_: zz_r[k_] for k_ in ("left", "in_pads", "caught", "caught_uv", "touch")}, "pad", np.round(pad_mid("right"), 3).tolist(), "pad_low", round(pad_low("right"), 3),
          "976", zz_in_pads("right", 976)[0], "hamper", np.round(hc_, 3).tolist(), "who", contact_report()["body_who"], flush=True)
    if zz_r["touch"] > 3.0:
        break
print("look", zz_look(pad_mid("right"), "regrasp_down", dist=0.6, h=0.35, dirs=(60.0, 150.0, 240.0), top=True), flush=True)
