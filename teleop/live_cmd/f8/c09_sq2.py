mon_start(target=None); MON["ignore_names"] = (zz_cb,)
try:
    PRE_ACTION("squat_follow", dict(h=-0.30))
    squat_follow(("left",), -0.30, 0.40, T=1.4)
    print("squat2", state(), "pad", np.round(pad_mid("left"), 3).tolist(), "stock", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
    for k_ in range(3):
        if in_container(zz_n, zz_cb)["lowest"] < 0.03 or pad_mid("left")[2] < 0.22:
            break
        r_ = thand("left", dz=-0.04, frame="world", Q={"left": q_(ts.ee_pose("left")[1])}, tag="stock_down3")
        print("down", r_["grip_pt"], r_["err"], "stock", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "stock_down3_end"), state(), flush=True)
