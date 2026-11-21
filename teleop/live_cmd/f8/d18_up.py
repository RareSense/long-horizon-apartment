mon_start(target=None); MON["ignore_names"] = (body_of("r130i1_light_saber"),); MON["start"].pop(zz_s, None)
MON["lim_hand"] = 200.0
try:
    for k_ in range(3):
        r_ = thand("left", dz=0.04, frame="world", tag="sc_left_up")
        print("left", r_["grip_pt"], r_["err"], "touch", contact_report(), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
G_, fwd_, SP_ = sc_grip_points(zz_s)
print("bar c", np.round(SP_["bar_c"], 3).tolist(), "pad left", np.round(pad_mid("left"), 3).tolist(), "wrist", np.round(ts.ee_pose("left")[0], 3).tolist(), flush=True)
