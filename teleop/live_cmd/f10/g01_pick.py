exec(open(r"E:\urc_fable3\scripts\home\island_skills.py", encoding="utf-8").read())
exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
def zz_others():
    return [c_ for c_ in _thing_contacts(pb_) if "Dex1" not in c_ and "wrist" not in c_]
zz_out = {}
rest_hands(SIDES)
mon_start(target=None)
try:
    w_ = walk_tight((-5.87, -2.20, np.pi))
    zz_out["walk"] = {k_: w_.get(k_) for k_ in ("ok", "err_xy")}
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
    zz_out.update(eR=np.round(eR_, 3).tolist(), eL=np.round(eL_, 3).tolist(), pouch_x=round(xc_, 3))
    u_ = pad_mid("right") - pad_mid("left"); u_[2] = 0.0; u_ /= np.linalg.norm(u_)          # left hand -> right hand
    PRE_ACTION("two_hand_squeeze", dict(force=10.0))
    r_ = op.squeeze("right", "left", u_, 10.0, speed=0.03, max_travel=0.08, friction=1.2)
    TWO["on"] = True; two_keep(0.5)
    zz_out["squeeze"] = dict(ok=r_.get("ok"), F={s_: zz_force(s_) for s_ in SIDES}, others=zz_others(), check=two_hand_check(pb_))
    print("squeezed", zz_out, flush=True)
    if all(zz_force(s_) > 2.0 for s_ in SIDES):
        z0_ = float(centre(pb_)[2])
        PRE_ACTION("two_hand_lift", dict(dz=0.05))
        op.carry((0.0, 0.0, 0.03), 0.05 / 0.03, object_mass=float(m.body_subtreemass[m.body(pb_).id])); two_keep(0.5)
        zz_out["lift"] = dict(rose=round(float(centre(pb_)[2]) - z0_, 3), F={s_: zz_force(s_) for s_ in SIDES}, others=zz_others())
        if zz_out["lift"]["rose"] > 0.035 and not zz_out["lift"]["others"] and all(zz_force(s_) > 1.0 for s_ in SIDES):
            hold_on("left", pb_, 0.5); hold_on("right", pb_, 0.5)      # contact-verified: lifted by both hands' friction, only the hands touch it
            HELD["left"] = dict(two=True); HELD["right"] = dict(two=True)
            MON["held"] = {"left": pb_, "right": pb_}; MON["last_touch"] = {}
            ts.walk_hand_weight = 20.0; op._hold.pop("base_prev", None)
            zz_out["hold"] = True
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
