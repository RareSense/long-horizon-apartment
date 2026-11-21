ZZ_F = 4.0
zz_out = {}
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = (zz_b,); MON["ignore"] = {m.body(zz_b).id}
try:
    u2_ = pad_mid("right") - pad_mid("left"); u2_[2] = 0.0; u2_ /= np.linalg.norm(u2_)
    PRE_ACTION("two_hand_squeeze", dict(force=ZZ_F))
    r_ = op.squeeze("right", "left", u2_, ZZ_F, speed=0.02, max_travel=0.08, friction=1.2)
    print("squeeze r", {k_: v_ for k_, v_ in r_.items() if k_ in ("ok", "error", "width", "touch")}, flush=True)
    if not r_.get("ok"):
        raise Abort("squeeze: " + str(r_.get("error")))
    TWO["on"] = True; two_keep(0.5)
    zz_out["squeeze"] = dict(ok=r_.get("ok"), F={s_: zz_force(s_, zz_b) for s_ in SIDES}, others=zz_others(zz_b), bag=np.round(centre(zz_b), 3).tolist(),
                             tilt=round(float(np.degrees(np.arccos(np.clip(abs(d.xmat[m.body(zz_b).id].reshape(3, 3)[2, 2]), -1, 1)))), 1))
    print("squeezed", zz_out, flush=True)
    if all(zz_force(s_, zz_b) > 0.5 for s_ in SIDES):
        z0_ = float(centre(zz_b)[2])
        PRE_ACTION("two_hand_lift", dict(dz=0.05))
        op.carry((0.0, 0.0, 0.03), 0.05 / 0.03, object_mass=float(m.body_subtreemass[m.body(zz_b).id])); two_keep(0.5)
        zz_out["lift"] = dict(rose=round(float(centre(zz_b)[2]) - z0_, 3), F={s_: zz_force(s_, zz_b) for s_ in SIDES}, others=zz_others(zz_b),
                              tilt=round(float(np.degrees(np.arccos(np.clip(abs(d.xmat[m.body(zz_b).id].reshape(3, 3)[2, 2]), -1, 1)))), 1))
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "bag", np.round(centre(zz_b), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print(look_hand("right", "n1_bag_lift"), flush=True)
