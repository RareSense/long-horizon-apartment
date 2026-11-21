zz_b = body_of("r124i1_sandal")
zz_Q = {"left": q_(ts.ee_pose("left")[1])}
mon_start(target=None); MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
try:
    for zz_t in ((0.0, 0.30, 0.62), (0.15, 0.29, 0.55)):
        PRE_ACTION("bc_hand", dict(side="left", to=list(zz_t)))
        e_ = bc_pads_to("left", bc_rf(zz_t), Q=zz_Q, speed=0.08, step=0.05)
        print("hand to", zz_t, "err", e_, "sandal", np.round(centre(zz_b), 3).tolist(), "touch", contact_report(), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("look", look_hand("left", "sandal_hand_ahead"), flush=True)
