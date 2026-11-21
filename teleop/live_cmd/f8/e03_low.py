mon_start(target=None); MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time)
zz_Q = {"right": q_(ts.ee_pose("right")[1])}
try:
    PRE_ACTION("squat_follow", dict(h=-0.38, l=0.8))
    squat_follow(("right",), -0.38, 0.8, T=1.4)
    print("squat", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "flat", np.round(centre(zz_b), 3).tolist(), "bottom", round(float(obj_box(zz_b)[0][2]), 3), "touch", contact_report(), flush=True)
    for k_ in range(6):
        c_ = centre(zz_b); lo_ = float(obj_box(zz_b)[0][2])
        e_ = np.array([1.22, -2.26]) - c_[:2]
        if lo_ < 0.022 and np.linalg.norm(e_) < 0.02: break
        dz_ = -min(0.04, max(0.0, lo_ - 0.015))
        r_ = thand("right", dx=float(np.clip(e_[0], -0.03, 0.03)), dy=float(np.clip(e_[1], -0.03, 0.03)), dz=dz_, frame="world", Q=zz_Q, tag="flat_down")
        print("down", r_["grip_pt"], r_["err"], "flat", np.round(centre(zz_b), 3).tolist(), "bottom", round(float(obj_box(zz_b)[0][2]), 3), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("flat box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "state", state(), "tilt", round(pelvis_tilt(), 3), flush=True)
print(look_hand("right", "flat_low"), flush=True)
