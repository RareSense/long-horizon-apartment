# two-hand paddle squeeze helpers (from f10 e02/g01, toy pouch, coordinator-approved contact-verified two-hand hold). AI-operated.
exec(open(r"E:\urc_final\scripts\home\island_skills.py", encoding="utf-8").read())
def zz_force(sd, pb_):
    import mujoco as _mj
    f_ = 0.0; c6_ = np.zeros(6); M_, D_ = br.mjm, br.mjd
    hb_ = set(i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith((sd + "_Dex1_base_link", sd + "_Dex1_finger_link_1", sd + "_Dex1_finger_link_2", sd + "_wrist_yaw_link")))
    pid2_ = [i_ for i_ in range(M_.nbody) if M_.body(i_).name.endswith("_" + pb_)][0]
    for i_ in range(D_.ncon):
        c_ = D_.contact[i_]; b1_ = int(M_.geom_bodyid[c_.geom1]); b2_ = int(M_.geom_bodyid[c_.geom2])
        if (b1_ == pid2_ and b2_ in hb_) or (b2_ == pid2_ and b1_ in hb_):
            _mj.mj_contactForce(M_, D_, i_, c6_); f_ += abs(float(c6_[0]))
    return round(f_, 2)
def zz_others(pb_):
    return [c_ for c_ in _thing_contacts(pb_) if "Dex1" not in c_ and "wrist" not in c_]
print("[two_lib] loaded", flush=True)
