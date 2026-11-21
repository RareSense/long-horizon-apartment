exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
zz_in = {"left": np.array([0.0, 1.0, 0.0]), "right": np.array([0.0, -1.0, 0.0])}
mon_start(target=pb_); MON["ignore_names"] = (pb_,)
try:
    z0_ = float(centre(pb_)[2])
    for k_ in range(3):
        tg_ = {s_: (ts.ee_pose(s_)[0] + 0.002 * zz_in[s_] + np.array([0, 0, 0.02])).tolist() for s_ in SIDES}
        PRE_ACTION("lift_both", dict(k=k_)); op.move(tg_, speed=0.02, quats=zz_Q, timeout=2.0, tol=0.003); op.run(0.3)
        print("lift", k_, "rose", round(float(centre(pb_)[2]) - z0_, 3), "forces", {s_: zz_force(s_) for s_ in SIDES}, "pouch", np.round(centre(pb_), 3).tolist(), "pads z", round(float(pad_mid("left")[2]), 3), round(float(pad_mid("right")[2]), 3), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
zz_c = centre(pb_)
print("state", state(), "touch", contact_report(), "fell", fallen(), flush=True)
print(close(os.path.join(TELE_DIR, "pouch_lift.jpg"), zz_c + np.array([0.45, -0.25, 0.25]), zz_c, "pouch lift"), flush=True)
