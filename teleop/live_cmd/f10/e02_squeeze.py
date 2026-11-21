# two-hand squeeze of the toy pouch (11 cm across, wider than one jaw's 7.9 cm opening): closed jaws fingers down as paddles
pb_ = body_of("r179i1_toy_pouch"); pid_ = m.body(pb_).id
zz_Q = {s_: q_(R_down([0.0, 1.0])) for s_ in SIDES}
zz_X = globals().get("ZZ_X", -6.15); zz_Z = globals().get("ZZ_Z", 0.83)
def zz_f(sd):
    t_ = finger_touch(sd); return t_
def zz_force(sd):
    import mujoco as _mj
    hb_ = set(i_ for i_ in range(m.nbody) if m.body(i_).name.startswith(sd + "_Dex1") or m.body(i_).name.startswith(sd + "_wrist"))
    f_ = 0.0; c6_ = np.zeros(6)
    M_, D_ = br.mjm, br.mjd
    hb_ = set(i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith((sd + "_Dex1_base_link", sd + "_Dex1_finger_link_1", sd + "_Dex1_finger_link_2", sd + "_wrist_yaw_link")))
    pid2_ = [i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith("_" + pb_)][0]
    for i_ in range(D_.ncon):
        c_ = D_.contact[i_]; b1_ = int(M_.geom_bodyid[c_.geom1]); b2_ = int(M_.geom_bodyid[c_.geom2])
        if (b1_ == pid2_ and b2_ in hb_) or (b2_ == pid2_ and b1_ in hb_):
            _mj.mj_contactForce(M_, D_, i_, c6_); f_ += abs(float(c6_[0]))
    return round(f_, 2)
mon_start(target=pb_); MON["ignore_names"] = (pb_,)
zz_out = {}
try:
    lo_, hi_ = obj_box(pb_)
    yS_, yN_ = float(lo_[1]), float(hi_[1])
    PRE_ACTION("close_jaws", {}); close_jaws("left", 10.0, T=0.4); close_jaws("right", 10.0, T=0.4)
    PRE_ACTION("crouch", {}); crouch(0.0, 0.3, T=1.5)
    PRE_ACTION("hands_above", {})
    servo_pads("right", np.array([zz_X, yN_ + 0.04]), zz_Z + 0.12, zz_Q, speed=0.15, n=2)
    servo_pads("left", np.array([zz_X, yS_ - 0.04]), zz_Z + 0.12, zz_Q, speed=0.15, n=2)
    PRE_ACTION("hands_down", {})
    eR_ = servo_pads("right", np.array([zz_X, yN_ + 0.035]), zz_Z, zz_Q, speed=0.06, n=3)
    eL_ = servo_pads("left", np.array([zz_X, yS_ - 0.035]), zz_Z, zz_Q, speed=0.06, n=3)
    zz_out.update(eR=np.round(eR_, 3).tolist(), eL=np.round(eL_, 3).tolist(), padR=np.round(pad_mid("right"), 3).tolist(), padL=np.round(pad_mid("left"), 3).tolist(), y_faces=(round(yS_, 3), round(yN_, 3)))
    print("down", zz_out, "forces", zz_force("left"), zz_force("right"), "state", state(), flush=True)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "touch", contact_report()["body"], "fell", fallen(), flush=True)
print(look_hand("right", "pouch_hands_down"), flush=True)
zz_c = centre(pb_)
print(close(os.path.join(TELE_DIR, "pouch_top.jpg"), zz_c + np.array([0.45, 0.10, 0.40]), zz_c, "pouch hands"), flush=True)
