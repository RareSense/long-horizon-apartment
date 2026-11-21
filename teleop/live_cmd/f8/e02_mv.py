zz_b = body_of("r125i2_flat")
mon_start(target=None); MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time)
zz_Q = {"right": q_(ts.ee_pose("right")[1])}
try:
    for k_ in range(3):
        e_ = np.array([1.16, -2.27]) - centre(zz_b)[:2]
        if np.linalg.norm(e_) < 0.015: break
        r_ = thand("right", dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), frame="world", Q=zz_Q, tag="flat_to_spot")
        print("mv", r_["grip_pt"], r_["err"], "flat", np.round(centre(zz_b), 3).tolist(), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
lo_, hi_ = obj_box(zz_b)
print("flat box", [np.round(v_, 3).tolist() for v_ in (lo_, hi_)], "state", state(), "tilt", round(pelvis_tilt(), 3), flush=True)
