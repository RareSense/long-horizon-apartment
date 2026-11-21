zz_sp = np.array([1.50, -2.04])
mon_start(target=None); MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time)
zz_Q = {"right": q_(ts.ee_pose("right")[1])}
def zz_toward(zmin, n=6):
    for k_ in range(n):
        c_ = centre(zz_b); lo_ = float(obj_box(zz_b)[0][2]); e_ = zz_sp - c_[:2]
        if lo_ < zmin and np.linalg.norm(e_) < 0.02: break
        dz_ = -min(0.04, max(0.0, lo_ - zmin))
        r_ = thand("right", dx=float(np.clip(e_[0], -0.04, 0.04)), dy=float(np.clip(e_[1], -0.04, 0.04)), dz=dz_, frame="world", Q=zz_Q, tag="flat1_put")
        print("mv", r_["grip_pt"], r_["err"], "flat", np.round(centre(zz_b), 3).tolist(), "bottom", round(float(obj_box(zz_b)[0][2]), 3), "box", [np.round(v_, 2).tolist() for v_ in obj_box(zz_b)], "touch", contact_report()["body"], flush=True)
try:
    zz_toward(0.6, n=5)
    for hh_, ll_ in ((-0.30, 0.6), (-0.38, 0.8)):
        PRE_ACTION("squat_follow", dict(h=hh_, l=ll_)); squat_follow(("right",), hh_, ll_, T=1.4)
        print("squat", state()["pelvis"], "flat", np.round(centre(zz_b), 3).tolist(), "bottom", round(float(obj_box(zz_b)[0][2]), 3), "touch", contact_report(), flush=True)
        if float(obj_box(zz_b)[0][2]) < 0.03: break
    zz_toward(0.022, n=6)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("flat box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "state", state(), flush=True)
print(look_hand("right", "flat1_low"), flush=True)
