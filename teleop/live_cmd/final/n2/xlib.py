# helpers for the final-sweep fix (AI-operated, 21 Nov): floor corner pinch next to the bin, carry to 0.40 m south, servo over the middle, drop
def x_over_bin(pb_):
    bn_ = body_of("rubbish_bin"); rc_ = obj_rect("rubbish_bin"); P_ = GG.body_points(m, d, m.body(pb_).id)
    q_l = np.abs((P_[:, :2] - rc_.c) @ rc_.R); hi_ = obj_box(bn_)[1]
    return bool(np.all(q_l < rc_.h - 0.025) and P_[:, 2].min() > hi_[2] + 0.01)

def x_pick(nm_, SD, far_from_bin=True):
    pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); CK_STATE["item"] = "fix_" + nm_
    C_ = flat_corners(pb_)[0]; bc_ = centre(bn_)[:2]
    G_ = np.asarray(max(C_, key=lambda c_: np.linalg.norm(np.asarray(c_) - bc_)), float)
    sg_ = -1.0 if SD == "right" else 1.0
    st_ = (float(G_[0] + sg_ * 0.20), float(G_[1] - 0.25), np.pi / 2)
    print(nm_, "corners", np.round(C_, 3).tolist(), "far", np.round(G_, 3).tolist(), "stance", np.round(st_, 3).tolist(), flush=True)
    mon_start(target=None)
    try:
        walk_tight(st_)
    except (Abort, RuntimeError) as ex_:
        print("walk ERR", str(ex_)[:200], flush=True)
    MON["on"] = False
    print("at", state(), "corner rel", np.round(rel(np.r_[G_, 0.0]), 3).tolist(), flush=True)
    mon_start(target=pb_)
    try:
        for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
            crouch(hh_, ll_, T=1.2)
    except Abort as ex_:
        print("squat abort", ex_, flush=True)
    MON["on"] = False
    c_ = corner_pick(nm_, SD, s_in=0.018, force=8.0); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
    return HOLD.holding(SD)

def x_drop(nm_, SD):
    pb_ = body_of(nm_); bn_ = body_of("rubbish_bin")
    print("ck", ck_save("x_held_" + nm_, kind="act", info=dict(note=f"{nm_} held again by a corner pinch from the floor (AI-operated)")), flush=True)
    mon_start(target=None); MON["held"][SD] = pb_; MON["last_touch"][SD] = float(d.time); MON["t_max"] = 900.0
    try:
        crouch_holding((SD,), H_WALK, 0.0, T=2.0)
        bc_ = centre(bn_)
        globals()["CARRY_JOINTS"] = True
        walk_tight((float(bc_[0]) - 0.03, float(bc_[1]) - 0.40, np.pi / 2), carry=(SD,))
    except (Abort, RuntimeError) as ex_:
        print("carry ERR", str(ex_)[:300], flush=True)
    finally:
        globals()["CARRY_JOINTS"] = False
    MON["on"] = False
    if not HOLD.holding(SD):
        return False
    print("ck", ck_save("x_at_bin_" + nm_, kind="act", info=dict(note=f"{nm_} at the bin stance 0.40 m south (AI-operated)")), flush=True)
    mon_start(target=None); MON["held"][SD] = pb_; MON["last_touch"][SD] = float(d.time)
    try:
        Qp = {SD: q_(ts.ee_pose(SD)[1])}
        for it_ in range(4):
            dlt_ = centre(bn_)[:2] - centre(pb_)[:2]
            if x_over_bin(pb_) and np.linalg.norm(dlt_) < 0.03:
                break
            PRE_ACTION("servo_pads", dict(it=it_)); servo_pads(SD, pad_mid(SD)[:2] + dlt_, float(pad_mid(SD)[2]), Qp, speed=0.05)
        print("over", x_over_bin(pb_), np.round(centre(pb_), 3).tolist(), flush=True)
        if x_over_bin(pb_):
            MON["ignore_names"] = (pb_,); MON["start"].pop(pb_, None)
            PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(1.5)
            hp_ = ts.ee_pose(SD)[0]; op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.1, timeout=2.0, tol=0.02)
            rest_hands(SIDES, T=0.6); op.run(0.5)
    except Abort as ex_:
        print("drop abort", ex_, flush=True)
    MON["on"] = False
    return not HOLD.holding(SD)

def x_back():
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.3)); op.run(0.4)
    mon_start(target=None)
    for k_ in range(2):
        try:
            tmove(fwd=-0.10, tag="off_bin_tall")
        except Abort as ex_:
            print("off abort", ex_, flush=True)
    MON["on"] = False
    rest_hands(SIDES); op.run(0.5)

def x_report(tag):
    bn_ = body_of("rubbish_bin")
    print("bin", np.round(centre(bn_), 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), "state", state(), "fell", fallen(), "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "rec", rec.n, flush=True)
    for n_ in ("r149i1_pouch", "r195i3_paper", "r195i1_paper", "r158i1_tissue"):
        print(" ", n_, np.round(centre(body_of(n_)), 3).tolist(), "inside", inside(body_of(n_), bn_), flush=True)
    print(look3(tag), flush=True)
