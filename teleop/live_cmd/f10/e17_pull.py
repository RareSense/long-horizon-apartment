ck_load(os.path.join(RUN, "checkpoints", "0104_act_pull_in")); gait_on(); op.run(0.3)
exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
zz_in = {"left": np.array([0.0, 1.0, 0.0]), "right": np.array([0.0, -1.0, 0.0])}
def zz_resq(fmin=4.0, n=6):
    for j_ in range(n):
        f_ = {s_: zz_force(s_) for s_ in SIDES}
        low_ = [s_ for s_ in SIDES if f_[s_] < fmin]
        if not low_: return f_
        tg_ = {s_: (ts.ee_pose(s_)[0] + (0.002 * zz_in[s_] if s_ in low_ else 0.0)).tolist() for s_ in SIDES}
        op.move(tg_, speed=0.02, quats=zz_Q, timeout=1.0, tol=0.0015); op.run(0.15)
    return {s_: zz_force(s_) for s_ in SIDES}
print("loaded: pouch", np.round(centre(pb_), 3).tolist(), "forces", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
mon_start(target=None); MON["held"] = {"left": pb_, "right": pb_}; MON["last_touch"] = {s_: float(d.time) for s_ in SIDES}
try:
    print("resq", zz_resq(), flush=True)
    for k_ in range(ZZ_N):
        tg_ = {s_: (ts.ee_pose(s_)[0] + np.array([0.01, 0, 0.0])).tolist() for s_ in SIDES}
        PRE_ACTION("pull_in", dict(k=k_)); op.move(tg_, speed=0.02, quats=zz_Q, timeout=1.5, tol=0.002); op.run(0.15)
        f_ = zz_resq()
        print("pull", k_, "pouch", np.round(centre(pb_), 3).tolist(), "bottom", round(float(obj_box(pb_)[0][2]), 3), "forces", f_, "pads y", round(float(pad_mid("left")[1]), 3), round(float(pad_mid("right")[1]), 3), flush=True)
        if float(obj_box(pb_)[0][2]) < 0.745:
            print("pouch down: stop", flush=True); break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
