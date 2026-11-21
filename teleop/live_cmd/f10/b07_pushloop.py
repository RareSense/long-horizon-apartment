zz_b = body_of("r175i1_cardboard_box"); zz_Q = {"left": q_(R_down([1.0, 0.0]))}
zz_X = globals().get("ZZ_X", -5.14); zz_Z = globals().get("ZZ_Z", 0.05); zz_N = globals().get("ZZ_N", 14)
def zz_tilt():
    R_ = d.xmat[m.body(zz_b).id].reshape(3, 3)
    return round(float(np.degrees(np.arccos(np.clip(np.max(np.abs(R_[2, :])), -1, 1)))), 1)
mon_start(target=None); MON["ignore_names"] = (zz_b,)
try:
    for k_ in range(zz_N):
        c_ = centre(zz_b)
        if c_[1] >= 1.555:
            break
        hp_ = pad_mid("left")
        PRE_ACTION("push", dict(k=k_))
        servo_pads("left", np.array([zz_X, hp_[1] + 0.03]), zz_Z, zz_Q, speed=0.04, n=2)
        c2_ = centre(zz_b); lo_, hi_ = obj_box(zz_b)
        print("push", k_, "hand", np.round(pad_mid("left"), 3).tolist(), "box c", np.round(c2_, 3).tolist(), "y", round(float(lo_[1]), 3), round(float(hi_[1]), 3), "tilt", zz_tilt(), "touch", contact_report()["body"], "pelvis", state()["pelvis"], state()["yaw_deg"], flush=True)
        if zz_tilt() > 4.0:
            print("box tilts: stop", flush=True); break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("box", np.round(centre(zz_b), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "tilt", zz_tilt(), "state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
print(look3("box_after_push"), flush=True)
