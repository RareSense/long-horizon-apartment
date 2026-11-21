pb_ = body_of("r179i1_toy_pouch"); zz_Q = {s_: q_(R_down([0.0, 1.0])) for s_ in SIDES}
mon_start(target=pb_); MON["ignore_names"] = (pb_,)
try:
    PRE_ACTION("hands_up", {})
    for s_ in SIDES:
        hp_ = pad_mid(s_); servo_pads(s_, hp_[:2] + np.array([0.06, 0.0]), 0.98, zz_Q, speed=0.10, n=2)
    rest_hands(SIDES); crouch(0.0, 0.0, T=1.2)
    r_ = tmove(fwd=ZZ_F, tag="pouch_step")
    print("step", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "pouch rel", np.round(rel(centre(pb_)), 3).tolist(), "fell", fallen(), flush=True)
