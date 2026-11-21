mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = tuple(b_ for b_ in INFO["bodies"] if b_ == pb_ or b_ == bk_ or inside(b_, bk_)); MON["ignore"] = {m.body(pb_).id}
try:
    PRE_ACTION("two_hand_lower", {})
    S["dz_goal"] = S["dz"] - 0.15
    for k_ in range(44):
        op.run(0.25, [cmd])
        if zz_touch(): break
    print("arms: bottom", round(float(obj_box(pb_)[0][2]), 3), "err", np.round(xy_ - centre(pb_)[:2], 3).tolist(), "touch", zz_touch(), {s_: zz_force(s_) for s_ in SIDES}, "dz", round(S["dz"], 3), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
