rec.still_every = 300
nm = "r149i1_pouch"; pb_ = body_of(nm); SD = "right"; bn_ = body_of("rubbish_bin")
_start_item(nm)
mon_start(target=pb_)
try:
    walk_tight((-2.88, float(centre(pb_)[1]) - 0.20, np.pi))
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("at", state(), "pouch", np.round(centre(pb_), 3).tolist(), "rel", np.round(rel(centre(pb_)), 3).tolist(), flush=True)
print("ck", ck_save("n1_pouch149_east", kind="act", info=dict(note="east of the coffee table for pouch r149 (AI-operated)")), flush=True)
try:
    crouch(*surface_posture(0.47), T=1.2)
except Abort as ex_:
    print("posture abort", ex_, flush=True)
c_ = corner_pick(nm, SD, s_in=0.018, force=8.0); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
if c_.get("held"):
    print("ck", ck_save("n1_pouch149_held", kind="act", info=dict(note="pouch r149 held (guarded corner pinch) (AI-operated)")), flush=True)
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
    if HOLD.holding(SD):
        print("ck", ck_save("n1_pouch149_at_bin", kind="act", info=dict(note="pouch r149 at the bin stance (AI-operated)")), flush=True)
        mon_start(target=None); MON["held"][SD] = pb_; MON["last_touch"][SD] = float(d.time)
        try:
            Qp = {SD: q_(ts.ee_pose(SD)[1])}
            PRE_ACTION("servo_pads", {}); servo_pads(SD, pad_mid(SD)[:2] + (centre(bn_)[:2] - centre(pb_)[:2]), float(pad_mid(SD)[2]), Qp, speed=0.05)
            lo_, hi_ = obj_box(bn_); plo_, phi_ = obj_box(pb_)
            over_ = bool(lo_[0] + 0.02 < plo_[0] and phi_[0] < hi_[0] - 0.02 and lo_[1] + 0.02 < plo_[1] and phi_[1] < hi_[1] - 0.02)
            print("over", over_, np.round(centre(pb_), 3).tolist(), flush=True)
            if over_:
                MON["ignore_names"] = (pb_,); MON["start"].pop(pb_, None)
                PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(1.5)
                hp_ = ts.ee_pose(SD)[0]; op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.1, timeout=2.0, tol=0.02)
                rest_hands(SIDES, T=0.6); op.run(0.5)
        except Abort as ex_:
            print("drop abort", ex_, flush=True)
        MON["on"] = False
        op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.3)); op.run(0.4)
        for k_ in range(2):
            try:
                tmove(fwd=-0.10, tag="off_bin_tall")
            except Abort as ex_:
                print("off abort", ex_, flush=True)
        rest_hands(SIDES); op.run(0.5)
print("pouch", np.round(centre(pb_), 3).tolist(), "inside", inside(pb_, bn_), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print("FIN", _finish(nm, "AI-operated night finisher: stance east of the coffee table facing west, seat/table posture (-0.12,0.45), corner_pick right 1.8 cm in at the nearest corner (guarded hold), walk_tight carrying to 0.40 m south of the bin, hand servoed over its middle standing, open, two tall steps back"), flush=True)
print(look3("n1_pouch149_end"), flush=True)
