ck_load(os.path.join(RUN, "checkpoints", "0304_act_put_down")); gait_on(); op.run(0.5); refresh_jointed_footprints()
zz_b = body_of("r178i1_ball"); zz_sd = "left"
print("loaded: grip", grip_check(zz_sd, zz_b), "holding", HOLD.holding(zz_sd), "state", state(), flush=True)
HELD[zz_sd] = dict(min_gap=0.004)
mon_start(target=None); MON["held"][zz_sd] = zz_b; MON["last_touch"][zz_sd] = float(d.time)
try:
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, carry=(zz_sd,), tag="ball_back")
        print("back", r_["at"], r_["yaw_deg"], r_["touch"], "grip", grip_check(zz_sd, zz_b).get("ok"), "ball", np.round(centre(zz_b), 3).tolist(), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
