zz_cb = body_of("r186i1_basket"); lo_, hi_ = obj_box(zz_cb); bc_ = (lo_ + hi_) / 2
print("state", state(), "touch", contact_report(), "saber", [np.round(v_, 2).tolist() for v_ in obj_box(body_of("r130i1_light_saber"))], flush=True)
mon_start(target=None); MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time); MON["ignore_names"] = (zz_cb,)
try:
    Q_ = {"right": q_(ts.ee_pose("right")[1])}
    for k_ in range(8):
        e_ = np.r_[bc_[:2] - pad_mid("right")[:2], 0.42 - pad_mid("right")[2]]
        if np.linalg.norm(e_) < 0.025: break
        r_ = thand("right", dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=float(np.clip(e_[2], -0.04, 0.04)), frame="world", Q=Q_, tag="duck_over")
        print("hand", r_["grip_pt"], r_["err"], "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("pad", np.round(pad_mid("right"), 3).tolist(), "basket", [np.round(v_, 3).tolist() for v_ in (lo_, hi_)], "duck low", round(float(obj_box(zz_b)[0][2]), 3), "state", state(), flush=True)
print(look_hand("right", "duck_over_basket"), flush=True)
