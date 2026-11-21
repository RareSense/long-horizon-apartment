nm_ = "r149i1_pouch"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); SD = "right"
print("ck", ck_save("x_pouch_held", kind="act", info=dict(note="pouch r149 held again by a corner pinch from the floor beside the bin (AI-operated)")), flush=True)
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
print("at bin", state(), "held", HOLD.holding(SD), "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
if HOLD.holding(SD):
    print("ck", ck_save("x_pouch_at_bin", kind="act", info=dict(note="pouch r149 at the bin stance 0.40 m south (AI-operated)")), flush=True)
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
print("pouch", np.round(centre(pb_), 3).tolist(), "inside", inside(pb_, bn_), "bin", np.round(centre(bn_), 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
for n_ in ("r195i3_paper", "r195i1_paper", "r158i1_tissue"):
    print(n_, np.round(centre(body_of(n_)), 3).tolist(), "inside", inside(body_of(n_), bn_), flush=True)
print(close(os.path.join(TELE_DIR, "x04_bin_top.jpg"), centre(bn_) + np.array([0.05, -0.05, 1.3]), centre(bn_), "bin top"), flush=True)
print(look3("x04_pouch_drop"), flush=True)
