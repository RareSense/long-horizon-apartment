zz_cb = body_of("r186i1_basket")
mon_start(target=None); MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time); MON["ignore_names"] = (zz_cb,)
try:
    r_ = tmove(turn=10.0, side=-0.12, carry=("right",), tag="duck_to_basket"); print("m1", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
    r_ = tmove(side=-0.11, carry=("right",), tag="duck_to_basket"); print("m2", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
    lo_, hi_ = obj_box(zz_cb); bc_ = (lo_ + hi_) / 2
    Q_ = {"right": q_(ts.ee_pose("right")[1])}
    for k_ in range(6):
        e_ = np.r_[bc_[:2] - pad_mid("right")[:2], 0.40 - pad_mid("right")[2]]
        if np.linalg.norm(e_) < 0.02: break
        r_ = thand("right", dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=float(np.clip(e_[2], -0.04, 0.04)), frame="world", Q=Q_, tag="duck_over")
        print("hand", r_["grip_pt"], r_["err"], "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("pad", np.round(pad_mid("right"), 3).tolist(), "basket c", np.round(bc_, 3).tolist(), "state", state(), flush=True)
print(look_hand("right", "duck_over_basket"), flush=True)
