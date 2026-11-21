MON["on"] = False
sb_ = body_of("r154i1_stick"); SDs = "right"; o_ = {}
mon_start(target=sb_)
try:
    lo_, hi_ = obj_box(sb_); c_ = centre(sb_)
    long_ = np.array([0.0, 1.0]) if (hi_[1] - lo_[1]) > (hi_[0] - lo_[0]) else np.array([1.0, 0.0])
    cd_ = np.array([-long_[1], long_[0]])                       # close across the stick
    p_, yaw_ = base(); fwd_ = np.array([np.cos(yaw_), np.sin(yaw_)])
    u_ = long_ if long_ @ fwd_ < 0 else -long_                  # fingertips tilted away from the robot along the stick
    TILTD = 40.0
    Qs = {SDs: q_(R_tilt(cd_, u_, TILTD))}
    o_["ahead"] = round(ahead_of_pelvis(c_), 3)
    open_jaws(SDs, T=0.3)
    h_, ln_ = surface_posture(float(hi_[2]))
    if h_ < -0.01 or ln_ > 0.01:
        PRE_ACTION("crouch", {}); crouch(h_, ln_, T=1.5)
    o_["posture"] = (h_, ln_)
    PRE_ACTION("above", {}); o_["e_above"] = np.round(servo_pads(SDs, c_[:2], hi_[2] + 0.06, Qs, speed=0.10), 3).tolist()
    # down in 4 mm steps until a finger touches the table (contact with furniture) or the pads are at the stick's middle
    zt_ = float(lo_[2] + 0.5 * (hi_[2] - lo_[2]))
    z_ = float(pad_mid(SDs)[2]); log_ = []
    while z_ > zt_ + 0.001:
        z_ = max(zt_, z_ - 0.004)
        servo_pads(SDs, c_[:2], z_, Qs, speed=0.03, n=2)
        tab_ = [k_ for k_ in umb_contacts(sb_) if k_[0].startswith(SDs + ":")]
        fr_ = contact_report()
        log_.append((round(float(pad_mid(SDs)[2]), 4), fr_["body"]))
        if fr_["body"] > 3.0:
            break
    o_["down"] = log_[-4:]
    PRE_ACTION("close_jaws", {}); close_jaws(SDs, 8.0, T=0.8)
    g_ = grip_check(SDs, sb_, min_gap=0.003)
    o_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N", "between")}; o_["fingers"] = len(jaw_fingers_on(SDs, sb_))
    if hold_on(SDs, sb_):
        HELD[SDs] = dict(min_gap=0.003); MON["held"][SDs] = sb_; MON["target"] = None; MON["last_touch"][SDs] = float(d.time)
        z0_ = float(centre(sb_)[2]); hp_ = ts.ee_pose(SDs)[0]
        PRE_ACTION("lift", {}); op.move({SDs: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.05, quats=Qs, timeout=3.0, tol=0.006); op.run(0.3)
        o_["rose"] = round(float(centre(sb_)[2]) - z0_, 3); o_["held"] = True
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(at=np.round(centre(sb_), 3).tolist(), state=state())
print("STICK", o_, flush=True)
pm_ = pad_mid(SDs)
print(close(os.path.join(TELE_DIR, "f12_stick_grip.jpg"), np.r_[pm_[:2] + np.array([0.3, -0.05]), pm_[2] + 0.12], np.r_[pm_[:2], pm_[2] - 0.02], "stick grip"), flush=True)
