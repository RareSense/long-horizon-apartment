exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
zz_out = {}
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = (pb_,); MON["ignore"] = {m.body(pb_).id}; MON["t_max"] = 900.0   # the monitor reads finger links only; this hold presses with the jaw bases (checked by zz_force)
try:
    fwd_ = RM.rz(base()[1])[:2, 0]
    PRE_ACTION("two_hand_back", {})
    op.carry((float(-0.03 * fwd_[0]), float(-0.03 * fwd_[1]), 0.01), 0.09 / 0.03); two_keep(0.4)
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=2.0)); op.run(2.5, [lambda: _two_cmds()])
    zz_out["upright"] = dict(F={s_: zz_force(s_) for s_ in SIDES}, pouch=np.round(centre(pb_), 3).tolist())
    print("upright", zz_out, flush=True)
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, carry=SIDES, tag="pouch2_back")
        print("back", r_["at"], r_["touch"]["body"], "pouch", np.round(centre(pb_), 3).tolist(), "F", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
    globals()["TWO_V"] = 0.10
    w_ = with_tight(lambda: two_hand_walk((-4.85, -1.05, -125.0), pb_), rb0=0.22, rf0=0.12)
    zz_out["walk"] = {k_: w_.get(k_) for k_ in ("ok", "err_xy", "err_yaw", "way_points")} if isinstance(w_, dict) else str(w_)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_out["err"] = str(ex_)[:300]
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "F", {s_: zz_force(s_) for s_ in SIDES}, "state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print(look3("pouch_at_basket"), flush=True)
