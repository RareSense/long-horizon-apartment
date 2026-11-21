rec.still_every = 300
nm = "r93i1_nugget"; zz_b = body_of(nm); SD = "right"; o_ = {}
_start_item(nm)
mon_start(target=None)
try:
    walk_tight((2.164, -0.70, np.pi / 2))
except (Abort, RuntimeError) as ex_:
    o_["walk"] = str(ex_)[:200]
MON["on"] = False
print("at", state(), "nugget", np.round(centre(zz_b), 3).tolist(), "rel", np.round(rel(centre(zz_b)), 3).tolist(), flush=True)
print("ck", ck_save("n1_nugget_stance", kind="act", info=dict(note="island stance for nugget r93 (AI-operated)")), flush=True)
mon_start(target=zz_b)
try:
    try:
        crouch(*surface_posture(0.92), T=1.2)
    except Exception as ex_:
        print("posture ERR", str(ex_)[:150], flush=True)
    p_, yaw_ = base(); fwd_ = np.array([np.cos(yaw_), np.sin(yaw_)])
    x_ = np.r_[fwd_, 0.0]; y_ = np.array([-fwd_[1], fwd_[0], 0.0]); Rl_ = np.column_stack([x_, y_, np.cross(x_, y_)])
    Q_ = {SD: q_(Rl_)}
    c_ = centre(zz_b); lo_, hi_ = obj_box(zz_b)
    zp_ = float(max(c_[2], lo_[2] + 0.014))
    open_jaws(SD, T=0.3)
    PRE_ACTION("hand_behind", {}); o_["e_behind"] = np.round(servo_pads(SD, c_[:2] - fwd_ * 0.12, zp_ + 0.03, Q_, speed=0.10), 3).tolist()
    PRE_ACTION("hand_level", {}); o_["e_level"] = np.round(servo_pads(SD, c_[:2] - fwd_ * 0.12, zp_, Q_, speed=0.05), 3).tolist()
    PRE_ACTION("hand_in", {}); o_["e_in"] = np.round(servo_pads(SD, c_[:2], zp_, Q_, speed=0.04), 3).tolist()
    if np.linalg.norm(o_["e_in"][:2]) < 0.012 and abs(o_["e_in"][2]) < 0.012:
        PRE_ACTION("close_jaws", {}); close_jaws(SD, 6.0, T=0.8)
        g1_ = grip_check(SD, zz_b, min_gap=0.004)
        o_["grip"] = {k: g1_[k] for k in g1_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}; o_["fingers"] = len(jaw_fingers_on(SD, zz_b))
        if g1_["ok"] and hold_on(SD, zz_b):
            HELD[SD] = dict(min_gap=0.004); MON["held"][SD] = zz_b; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
            z0_ = float(centre(zz_b)[2]); hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.05]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.006); op.run(0.3)
            hp_ = ts.ee_pose(SD)[0]
            PRE_ACTION("pull_back", {}); op.move({SD: [hp_[0] - fwd_[0] * 0.12, hp_[1] - fwd_[1] * 0.12, hp_[2]]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
            o_["rose"] = round(float(centre(zz_b)[2]) - z0_, 3); o_["held"] = not hold_lost(SD)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
print("NUG", o_, "at", np.round(centre(zz_b), 3).tolist(), "state", state(), flush=True)
if o_.get("held"):
    print("ck", ck_save("n1_nugget_held", kind="act", info=dict(note="nugget held, level hand (AI-operated)")), flush=True)
    try:
        crouch(0.0, 0.0, T=1.2)
    except Abort:
        pass
    R_ = basket_put(nm, SD, Q_)
    print("BASKET", R_, flush=True)
print("FIN", _finish(nm, "AI-operated night finisher (first chain's k02 recipe): island stance (2.16,-0.70) facing north, surface posture, level hand fingers forward, jaws closing sideways at the nugget's middle height from 12 cm behind, guarded hold, lift 5 cm, pull back, basket_put at (-4.85,-1.05,-125)"), flush=True)
print(look3("n1_nugget_end"), flush=True)
