mon_start(target=None)
try:
    PRE_ACTION("crouch", dict(h=0.0, l=0.0)); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.4); rest_hands(SIDES); op.run(1.0)
    r_ = tmove(fwd=0.08, tag="n1_bag_closer")
    print("closer", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
zz_b = body_of("r196i1_plastic_bag")
print("bag rel", np.round(rel(centre(zz_b)), 3).tolist(), "feet", {s_: np.round(d.xpos[m.body(s_ + "_ankle_roll_link").id][:2], 3).tolist() for s_ in SIDES}, "state", state(), flush=True)
