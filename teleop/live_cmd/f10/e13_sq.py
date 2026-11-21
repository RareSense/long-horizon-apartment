exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
mon_start(target=pb_); MON["ignore_names"] = (pb_,)
zz_in = {"left": np.array([0.0, 1.0, 0.0]), "right": np.array([0.0, -1.0, 0.0])}   # left hand is south of the pouch
zz_log = []
try:
    z0_ = float(centre(pb_)[2]); done_ = {s_: False for s_ in SIDES}
    for k_ in range(14):
        tg_ = {}
        for s_ in SIDES:
            p_ = ts.ee_pose(s_)[0]
            tg_[s_] = (p_ + (0.0 if done_[s_] else 0.005) * zz_in[s_]).tolist()
        PRE_ACTION("squeeze", dict(k=k_)); op.move(tg_, speed=0.02, quats=zz_Q, timeout=1.5, tol=0.002); op.run(0.2)
        f_ = {s_: zz_force(s_) for s_ in SIDES}
        for s_ in SIDES:
            done_[s_] = done_[s_] or f_[s_] >= 5.0
        zz_log.append((k_, f_, np.round(centre(pb_), 3).tolist()))
        print("sq", zz_log[-1], "pads y", round(float(pad_mid("left")[1]), 3), round(float(pad_mid("right")[1]), 3), flush=True)
        if all(done_.values()):
            break
    if all(done_.values()):
        tg_ = {s_: (ts.ee_pose(s_)[0] + 0.003 * zz_in[s_] + np.array([0, 0, 0.05])).tolist() for s_ in SIDES}
        PRE_ACTION("lift_both", {}); op.move(tg_, speed=0.03, quats=zz_Q, timeout=3.0, tol=0.004); op.run(0.5)
        print("lifted: rose", round(float(centre(pb_)[2]) - z0_, 3), "forces", {s_: zz_force(s_) for s_ in SIDES}, "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
zz_c = centre(pb_)
print("state", state(), "touch", contact_report(), "fell", fallen(), flush=True)
print(close(os.path.join(TELE_DIR, "pouch_sq.jpg"), zz_c + np.array([0.45, 0.10, 0.40]), zz_c, "pouch squeeze"), flush=True)
