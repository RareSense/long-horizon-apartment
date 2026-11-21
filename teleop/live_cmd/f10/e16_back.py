exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
zz_in = {"left": np.array([0.0, 1.0, 0.0]), "right": np.array([0.0, -1.0, 0.0])}
mon_start(target=None); MON["held"] = {"left": pb_, "right": pb_}; MON["last_touch"] = {s_: float(d.time) for s_ in SIDES}
try:
    tg_ = {s_: (ts.ee_pose(s_)[0] + 0.003 * zz_in[s_]).tolist() for s_ in SIDES}
    PRE_ACTION("squeeze_more", {}); op.move(tg_, speed=0.02, quats=zz_Q, timeout=1.5, tol=0.002); op.run(0.3)
    print("squeeze", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
    for k_ in range(3):
        tg_ = {s_: (ts.ee_pose(s_)[0] + np.array([0.035, 0, 0.0])).tolist() for s_ in SIDES}
        PRE_ACTION("pull_in", dict(k=k_)); op.move(tg_, speed=0.03, quats=zz_Q, timeout=2.0, tol=0.003); op.run(0.2)
        print("pull", k_, "pouch", np.round(centre(pb_), 3).tolist(), "bottom", round(float(obj_box(pb_)[0][2]), 3), "forces", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
    PRE_ACTION("stand_holding", {}); crouch_holding(SIDES, H_WALK, 0.0, T=2.0)
    print("stood", state()["pelvis"], "pouch", np.round(centre(pb_), 3).tolist(), "forces", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, carry=SIDES, tag="pouch_back")
        print("back", r_["at"], r_["yaw_deg"], r_["touch"], "pouch", np.round(centre(pb_), 3).tolist(), "forces", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), flush=True)
print(look3("pouch_back"), flush=True)
