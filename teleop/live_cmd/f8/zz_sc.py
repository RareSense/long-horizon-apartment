# Scooter carry with the jaws closing FORE-AFT round the bar (fingers down), AI-operated teleop variant of scooter.py.
# Why: with the fingers forward (pads above/below the round bar) the bar twists in the jaws at each turn step (pads
# 2-13 cm off after the third 6 deg step, left hand lost it, this session). Fore-aft pads take the yaw torque as normal force.
_R_FWD0 = globals().get("_R_FWD0") or R_fwd
def zz_Rdown_fwd(fwd):
    return R_down(np.asarray(fwd, float)[:2])

def zz_sc_on(b_, speed=0.15):
    G_, fwd_, SP_ = sc_grip_points(b_)
    Q_ = {s_: q_(zz_Rdown_fwd(fwd_)) for s_ in SIDES}
    for s_ in SIDES:
        jaw_force[s_] = 20.0; jaw_target[s_] = JAW_OPEN
    PRE_ACTION("sc_hands_to", dict(stage="up_behind"))
    both_move({s_: G_[s_] - np.r_[fwd_ * 0.14, 0.0] + np.array([0, 0, 0.12]) for s_ in SIDES}, Q_, speed=speed, tol=0.01)
    PRE_ACTION("sc_hands_to", dict(stage="above"))
    e1_ = both_move({s_: G_[s_] + np.array([0, 0, 0.10]) for s_ in SIDES}, Q_, speed=speed, tol=0.006)
    PRE_ACTION("sc_hands_to", dict(stage="on_down"))
    e2_ = both_move({s_: G_[s_] for s_ in SIDES}, Q_, speed=0.06, tol=0.005)
    return e1_, e2_

def zz_sc_release(b_):
    for s_ in SIDES:
        open_jaws(s_, T=0.05); HELD.pop(s_, None)
        ts.ctrl.ext.pop(f"hold_{s_}", None)
    op.run(0.4)
    _, fwd_, _ = sc_grip_points(b_)
    Q_ = {s_: q_(zz_Rdown_fwd(fwd_)) for s_ in SIDES}
    both_move({s_: pad_mid(s_) + np.array([0, 0, 0.10]) for s_ in SIDES}, Q_, speed=0.1, tol=0.01)
    both_move({s_: pad_mid(s_) - np.r_[fwd_ * 0.10, 0.0] for s_ in SIDES}, Q_, speed=0.1, tol=0.01)
    rest_hands()

def zz_sc_take(nm="r126i1_scooter", say=print):
    """Take + lift only (the turns are driven step by step after it). Returns a record."""
    global SC_NAME
    SC_NAME = nm; b_ = body_of(nm); out = dict(item=nm)
    globals()["R_fwd"] = zz_Rdown_fwd
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.8)
    e1, e2 = zz_sc_on(b_)
    out["hand_err"] = (str(e1)[:120], str(e2)[:120])
    SP_ = scooter_parts(b_)
    out["bar_ahead"] = round(float((SP_["bar_c"][:2] - base()[0][:2]) @ SP_["deck"][:2]), 3); out["pel_z"] = round(float(base()[0][2]), 3)
    out["look_open"] = look_hand("left", "sc_down_open")
    PRE_ACTION("sc_close", {})
    g_ = sc_close(b_, force=20.0)
    G_, _, _ = sc_grip_points(b_)
    out["grips"] = {s_: dict(gap=g_[s_].get("gap"), j1=g_[s_].get("jaw1_N"), j2=g_[s_].get("jaw2_N"), pad_err=round(float(np.linalg.norm(pad_mid(s_) - G_[s_])), 3)) for s_ in SIDES}
    out["look_closed"] = look_hand("left", "sc_down_closed")
    ok_ = all(v_["gap"] and v_["gap"] > 0.0015 and v_["j1"] > 1.5 and v_["j2"] > 1.5 and v_["pad_err"] < 0.03 for v_ in out["grips"].values())
    if not ok_:
        out["status"] = "grip failed"; return out
    for s_ in SIDES:
        jaw_target[s_] = 0.0; jaw_force[s_] = 20.0
        ts.ctrl.ext[f"hold_{s_}"] = (f"{s_}_wrist_yaw_link", np.array([0.165, 0.0, 0.0]), np.array([0.0, 0.0, -9.81 * SC_PARK["hand_kg"]]))
    op.run(0.3)
    MON["held"] = {s_: b_ for s_ in SIDES}; MON["target"] = None
    for s_ in SIDES:
        MON["last_touch"][s_] = float(d.time)
    PRE_ACTION("sc_lift", {})
    out["lift"] = sc_lift(b_, dz=0.03)
    ok_, t_, e_ = _sc_in_jaws(b_)
    out["lift"].update(in_jaws=ok_, touch=t_, pad_to_bar=e_)
    out["look_lift"] = look3("sc_down_lift")
    SC_REL.clear(); _sc_rel_save()
    out["status"] = "held" if ok_ else "bar out after lift"
    return out
