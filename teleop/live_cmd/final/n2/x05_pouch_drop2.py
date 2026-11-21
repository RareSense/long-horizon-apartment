nm_ = "r149i1_pouch"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); SD = "right"
r0_ = rec.n
ck_load(os.path.join(RUN, "checkpoints", "0327_act_x_pouch_at_bin")); gait_on(); settle_after_load(); refresh_jointed_footprints(); op.run(0.5)
CK_STATE["item"] = "fix_" + nm_
print("RELOADED 0327 at rec", rec.n, "(discard", r0_, "branch: over-check False, stepped back holding)", state(), "held", HOLD.holding(SD), "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
def over_bin_():
    rc_ = obj_rect("rubbish_bin"); P_ = GG.body_points(m, d, m.body(pb_).id)
    q_l = np.abs((P_[:, :2] - rc_.c) @ rc_.R); hi_ = obj_box(bn_)[1]
    return bool(np.all(q_l < rc_.h - 0.025) and P_[:, 2].min() > hi_[2] + 0.01), np.round(q_l.max(0), 3).tolist(), np.round(rc_.h, 3).tolist()
if HOLD.holding(SD):
    mon_start(target=None); MON["held"][SD] = pb_; MON["last_touch"][SD] = float(d.time)
    try:
        Qp = {SD: q_(ts.ee_pose(SD)[1])}
        for it_ in range(3):
            dlt_ = centre(bn_)[:2] - centre(pb_)[:2]
            ov_ = over_bin_(); print("pass", it_, "delta", np.round(dlt_, 3).tolist(), "over", ov_, flush=True)
            if ov_[0] and np.linalg.norm(dlt_) < 0.03:
                break
            PRE_ACTION("servo_pads", dict(it=it_)); servo_pads(SD, pad_mid(SD)[:2] + dlt_, float(pad_mid(SD)[2]), Qp, speed=0.05)
        ov_ = over_bin_(); print("over", ov_, np.round(centre(pb_), 3).tolist(), flush=True)
        if ov_[0]:
            MON["ignore_names"] = (pb_,); MON["start"].pop(pb_, None)
            PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(1.5)
            hp_ = ts.ee_pose(SD)[0]; op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.1, timeout=2.0, tol=0.02)
            rest_hands(SIDES, T=0.6); op.run(0.5)
    except Abort as ex_:
        print("drop abort", ex_, flush=True)
    MON["on"] = False
print("pouch", np.round(centre(pb_), 3).tolist(), "inside", inside(pb_, bn_), "held", HOLD.holding(SD), "bin", np.round(centre(bn_), 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
print(look3("x05_pouch_drop2"), flush=True)
