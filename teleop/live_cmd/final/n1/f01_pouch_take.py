exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\two_lib.py", encoding="utf-8").read())
_start_item("r179i1_toy_pouch")
pb_ = body_of("r179i1_toy_pouch"); zz_Q = {s_: q_(R_down([0.0, 1.0])) for s_ in SIDES}; ZZ_Z = 0.80
zz_out = {}
rest_hands(SIDES)
mon_start(target=None)
try:
    w_ = walk_tight((-5.87, -2.20, np.pi))
    zz_out["walk"] = {k_: w_.get(k_) for k_ in ("ok", "err_xy")} if isinstance(w_, dict) else str(w_)[:100]
    print("ck", ck_save("n1_pouch_stance", kind="act", info=dict(note="sill stance for toy pouch r179 (AI-operated)")), flush=True)
    MON["ignore_names"] = (pb_,)
    lo_, hi_ = obj_box(pb_); yS_, yN_ = float(lo_[1]), float(hi_[1]); xc_ = float(centre(pb_)[0])
    PRE_ACTION("close_jaws", {}); close_jaws("left", 10.0, T=0.4); close_jaws("right", 10.0, T=0.4)
    PRE_ACTION("crouch", {}); crouch(0.0, 0.3, T=1.5)
    PRE_ACTION("hands_above", {})
    servo_pads("right", np.array([xc_, yN_ + 0.04]), ZZ_Z + 0.12, zz_Q, speed=0.15, n=2)
    servo_pads("left", np.array([xc_, yS_ - 0.04]), ZZ_Z + 0.12, zz_Q, speed=0.15, n=2)
    PRE_ACTION("hands_down", {})
    eR_ = servo_pads("right", np.array([xc_, yN_ + 0.03]), ZZ_Z, zz_Q, speed=0.06, n=3)
    eL_ = servo_pads("left", np.array([xc_, yS_ - 0.03]), ZZ_Z, zz_Q, speed=0.06, n=3)
    zz_out.update(eR=np.round(eR_, 3).tolist(), eL=np.round(eL_, 3).tolist())
    u_ = pad_mid("right") - pad_mid("left"); u_[2] = 0.0; u_ /= np.linalg.norm(u_)
    PRE_ACTION("two_hand_squeeze", dict(force=10.0))
    r_ = op.squeeze("right", "left", u_, 10.0, speed=0.03, max_travel=0.08, friction=1.2)
    if not r_.get("ok"):
        raise Abort("squeeze: " + str(r_.get("error")))
    TWO["on"] = True; two_keep(0.5)
    zz_out["squeeze"] = dict(F={s_: zz_force(s_, pb_) for s_ in SIDES}, others=zz_others(pb_))
    if all(zz_force(s_, pb_) > 2.0 for s_ in SIDES):
        z0_ = float(centre(pb_)[2])
        PRE_ACTION("two_hand_lift", dict(dz=0.05))
        op.carry((0.0, 0.0, 0.03), 0.05 / 0.03, object_mass=float(m.body_subtreemass[m.body(pb_).id])); two_keep(0.5)
        zz_out["lift"] = dict(rose=round(float(centre(pb_)[2]) - z0_, 3), F={s_: zz_force(s_, pb_) for s_ in SIDES}, others=zz_others(pb_))
        if zz_out["lift"]["rose"] > 0.035 and not zz_out["lift"]["others"] and all(zz_force(s_, pb_) > 1.0 for s_ in SIDES):
            hold_on("left", pb_, 0.5); hold_on("right", pb_, 0.5)
            HELD["left"] = dict(two=True); HELD["right"] = dict(two=True)
            MON["held"] = {"left": pb_, "right": pb_}; MON["last_touch"] = {}
            ts.walk_hand_weight = 20.0; op._hold.pop("base_prev", None)
            zz_out["hold"] = True
except (Abort, RuntimeError) as ex_:
    zz_out["abort"] = str(ex_)[:300]
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print(look3("n1_pouch_take"), flush=True)
