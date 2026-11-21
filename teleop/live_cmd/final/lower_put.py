# lower_put(nm, SD, xy): AI teleop finish of a floor put (AI-operated): the held thing's middle over xy, staged squat with
# the hand following, lower until its bottom is down, open, hand up, stand, rest. Returns the check.
def lower_put(nm, SD, xy, note="", done=True):
    zz_b = body_of(nm); o_ = {}
    mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
    try:
        zz_Q = {SD: q_(ts.ee_pose(SD)[1])}
        for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
            c_ = centre(zz_b); e_ = np.asarray(xy, float) - c_[:2]
            PRE_ACTION("lp_over", dict(side=SD, e=np.round(e_, 3).tolist()))
            bc_pads_to(SD, pad_mid(SD) + np.r_[e_, 0.0], Q=zz_Q, speed=0.05, step=0.04)
            PRE_ACTION("squat_follow", dict(h=hh_, l=ll_)); squat_follow((SD,), hh_, ll_, T=1.4)
            for k_ in range(4):
                lo_ = float(obj_box(zz_b)[0][2])
                if lo_ < 0.025:
                    break
                dz_ = -min(0.04, lo_ - 0.015)
                PRE_ACTION("bc_hand", dict(side=SD, dz=dz_)); bc_pads_to(SD, pad_mid(SD) + np.array([0, 0, dz_]), Q=zz_Q, speed=0.04, step=0.04)
            if float(obj_box(zz_b)[0][2]) < 0.025:
                break
        o_["bottom"] = round(float(obj_box(zz_b)[0][2]), 3); o_["off_xy"] = np.round(np.asarray(xy) - centre(zz_b)[:2], 3).tolist()
        if o_["bottom"] < 0.03:
            MON["ignore_names"] = (zz_b,); MON["start"].pop(zz_b, None)
            PRE_ACTION("open_jaws", dict(side=SD)); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(0.5)
            bc_pads_to(SD, pad_mid(SD) + np.array([0, 0, 0.10]), speed=0.06, step=0.05)
            jaw_target[SD] = 0.0
            for hh_, ll_ in ((-0.20, 0.35), (0.0, 0.0)):
                PRE_ACTION("crouch", dict(h=hh_, l=ll_)); crouch(hh_, ll_, T=1.4)
            rest_hands(SIDES); op.run(1.0)
    except Abort as ex_:
        o_["abort"] = str(ex_)[:300]
    MON["on"] = False
    o_.update(at=np.round(centre(zz_b), 3).tolist(), state=state(), fell=fallen(), touch=contact_report()["body"], held={s_: HOLD.holding(s_) for s_ in SIDES}, check=item_check(nm))
    print("LOWER_PUT", o_, flush=True)
    if done and o_["check"].get("ok") and not fallen() and not any(o_["held"].values()):
        o_["done"] = tele_item_done(nm, note=note or "AI teleop finish: over the spot, staged squat, lowered, open, stand (AI-operated)")
        print("DONE", o_["done"], flush=True)
    return o_
