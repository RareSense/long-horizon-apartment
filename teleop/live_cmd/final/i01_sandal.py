# sandal r124i1 -> shoe mat (AI-operated): library pick_floor (left, guarded), stand, walk to the first chain's put stance
# (1.38,-2.08, 180 deg) carrying left, hand ahead, squat in stages, lower until the sole is down, open, stand (f7 c10-c15).
zz_n = "r124i1_sandal"; zz_b = body_of(zz_n); o_ = {}
CK_STATE["item"] = f"{POS + 1:03d}_{zz_n}"
if base()[0][0] < -1.6:
    exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\exit_pocket.py", encoding="utf-8").read())
print("sandal", np.round(centre(zz_b), 3).tolist(), "dest", DESC["destinations"].get(zz_n), "spot", DESC["spots"].get(zz_n), flush=True)
mon_start(target=zz_b)
try:
    back_off_container()
    try:
        pk_ = pick_floor(zz_b, "left")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_):
            raise
        pk_ = with_tight(lambda: pick_floor(zz_b, "left"))
    o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
except Abort as ex_:
    o_["abort_pick"] = str(ex_)[:300]
MON["on"] = False
print("PICK", o_, state(), flush=True)
SD = (o_.get("pick") or {}).get("side")
if (o_.get("pick") or {}).get("ok") and SD:
    HELD[SD] = pk_.get("grip") or {}
    mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
    try:
        PRE_ACTION("squat_follow", dict(h=0.0, l=0.0)); squat_follow((SD,), 0.0, 0.0, T=1.4); op.run(0.6)
        w_ = with_tight(lambda: walk_path((1.38, -2.08, np.pi), carry=(SD,), tol=0.04))
        o_["walk"] = w_.get("err_xy") if isinstance(w_, dict) else str(w_)[:100]
        print("at put stance", state(), "touch", contact_report(), flush=True)
        zz_Q = {SD: q_(ts.ee_pose(SD)[1])}
        sg_ = 1.0 if SD == "left" else -1.0
        for zz_t in ((0.0, sg_ * 0.30, 0.62), (0.15, sg_ * 0.29, 0.55)):
            PRE_ACTION("bc_hand", dict(side=SD, to=list(zz_t))); bc_pads_to(SD, bc_rf(zz_t), Q=zz_Q, speed=0.08, step=0.05)
        for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
            PRE_ACTION("squat_follow", dict(h=hh_, l=ll_)); squat_follow((SD,), hh_, ll_, T=1.4)
            for k_ in range(4):
                lo_ = float(obj_box(zz_b)[0][2])
                if lo_ < 0.025:
                    break
                dz_ = -min(0.04, lo_ - 0.015)
                PRE_ACTION("bc_hand", dict(side=SD, dz=dz_)); bc_pads_to(SD, pad_mid(SD) + np.array([0, 0, dz_]), Q=zz_Q, speed=0.04, step=0.04)
            if float(obj_box(zz_b)[0][2]) < 0.025:
                break
        o_["bottom"] = round(float(obj_box(zz_b)[0][2]), 3)
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
o_.update(sandal=np.round(centre(zz_b), 3).tolist(), state=state(), fell=fallen(), touch=contact_report(), held={s_: HOLD.holding(s_) for s_ in SIDES}, check=item_check(zz_n))
print("RES", o_, flush=True)
print(look3("sandal_end"), flush=True)
if o_["check"].get("ok") and not fallen() and not any(o_["held"].values()):
    print("DONE", tele_item_done(zz_n, note="pick_floor (guarded) + walk to (1.38,-2.08,180 deg) + hand ahead, staged squat, lowered until the sole is down, open, stand (first chain's teleop steps as one script; AI-operated)"), flush=True)
print("SAY", say_item(), flush=True)
