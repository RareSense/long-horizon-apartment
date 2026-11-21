zz_b = body_of("r175i1_cardboard_box"); zz_Q = {"left": q_(R_down([1.0, 0.0]))}
def zz_tilt():
    R_ = d.xmat[m.body(zz_b).id].reshape(3, 3)
    return round(float(np.degrees(np.arccos(np.clip(np.max(np.abs(R_[2, :])), -1, 1)))), 1)
mon_start(target=None); MON["ignore_names"] = (zz_b,)
try:
    hp_ = pad_mid("left")
    PRE_ACTION("hand_back", {}); servo_pads("left", np.array([hp_[0], hp_[1] - 0.04]), hp_[2] + 0.01, zz_Q, speed=0.03, n=2)
    op.run(1.0)
    print("released: box", np.round(centre(zz_b), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(zz_b)], "tilt", zz_tilt(), flush=True)
    PRE_ACTION("hand_up", {}); servo_pads("left", np.array([hp_[0], hp_[1] - 0.10]), 0.30, zz_Q, speed=0.08, n=2)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2)
    arms_to("rest", ["left"], T=1.0)
    open_jaws("left", T=0.3)
    r_ = tmove(fwd=-0.12, tag="box_back")
    print("back", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("box", np.round(centre(zz_b), 3).tolist(), "tilt", zz_tilt(), "state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print(close(os.path.join(TELE_DIR, "box_done.jpg"), np.r_[centre(zz_b)[:2] + np.array([0.9, -0.9]), 1.4], np.r_[centre(zz_b)[:2], 0.1], "box done"), flush=True)
