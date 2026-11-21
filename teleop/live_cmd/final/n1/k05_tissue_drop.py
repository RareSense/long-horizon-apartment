nm = "r158i1_tissue"; tb_ = body_of(nm); SD = "right"; bn_ = body_of("rubbish_bin")
ck_load(os.path.join(RUN, "checkpoints", [c_ for c_ in sorted(os.listdir(os.path.join(RUN, "checkpoints"))) if c_.endswith("_act_n1_tissue_at_bin")][-1])); gait_on(); op.run(0.5); refresh_jointed_footprints()
HELD[SD] = dict(min_gap=0.004)
print("RELOADED at_bin rec", rec.n, "holding", HOLD.holding(SD), "tissue", np.round(centre(tb_), 3).tolist(), "pad", np.round(pad_mid(SD), 3).tolist(), flush=True)
mon_start(target=None); MON["held"][SD] = tb_; MON["last_touch"][SD] = float(d.time)
try:
    Qp = {SD: q_(ts.ee_pose(SD)[1])}
    bc_ = centre(bn_); hz_ = float(pad_mid(SD)[2])
    PRE_ACTION("servo_pads", {}); e_ = servo_pads(SD, pad_mid(SD)[:2] + (bc_[:2] - centre(tb_)[:2]), hz_, Qp, speed=0.05)
    lo_, hi_ = obj_box(bn_); plo_, phi_ = obj_box(tb_)
    over_ = bool(lo_[0] + 0.03 < plo_[0] and phi_[0] < hi_[0] - 0.03 and lo_[1] + 0.03 < plo_[1] and phi_[1] < hi_[1] - 0.03)
    print("over", over_, "tissue", np.round(centre(tb_), 3).tolist(), "e", np.round(e_, 3).tolist(), flush=True)
    if over_:
        MON["ignore_names"] = (tb_,); MON["start"].pop(tb_, None)
        PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(1.5)
        hp_ = ts.ee_pose(SD)[0]; op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.06]}, speed=0.1, timeout=2.0, tol=0.02)
        rest_hands(SIDES, T=0.6); op.run(0.5)
        MON["ignore_names"] = (tb_, bn_)
        tmove(fwd=-0.10, tag="off_bin")
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("tissue", np.round(centre(tb_), 3).tolist(), "inside", inside(tb_, bn_), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print("FIN", _finish(nm, "AI-operated night finisher: stance (-2.83,-0.51,124 deg), seat posture (-0.12,0.45), corner_pick right s_in 2.5 cm force 5 N (guard passed, rose 10 cm); put_away found no path -> walk_tight carrying to 0.40 m south of the bin (hand already over it), hand servoed over the bin middle standing, open, hand up, step back"), flush=True)
print(look3("n1_tissue_in"), flush=True)
