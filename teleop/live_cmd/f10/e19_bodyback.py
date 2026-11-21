ck_load(os.path.join(RUN, "checkpoints", "0104_act_pull_in")); gait_on(); op.run(0.3)
exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
mon_start(target=None); MON["held"] = {"left": pb_, "right": pb_}; MON["last_touch"] = {s_: float(d.time) for s_ in SIDES}
print("ee modes", {k_: v_.get("mode") for k_, v_ in ts.ee.items()}, "pads", np.round(pad_mid("left"), 3).tolist(), np.round(pad_mid("right"), 3).tolist(), "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
try:
    for k_ in range(3):
        r_ = tmove(fwd=-0.06, carry=SIDES, tag="pouch_body_back")
        print("back", r_["at"], r_["yaw_deg"], r_["touch"]["body"], "pouch", np.round(centre(pb_), 3).tolist(), "bottom", round(float(obj_box(pb_)[0][2]), 3), "forces", {s_: zz_force(s_) for s_ in SIDES}, "pads", np.round(pad_mid("left"), 3).tolist(), np.round(pad_mid("right"), 3).tolist(), flush=True)
        if float(obj_box(pb_)[0][2]) < 0.745: break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
