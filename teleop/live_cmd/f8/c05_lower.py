mon_start(target=None); MON["ignore_names"] = (zz_cb,); MON["held"] = {}
try:
    PRE_ACTION("squat_follow", dict(h=-0.20))
    squat_follow(("left",), -0.20, 0.15, T=1.6)
    print("squat", state(), "pad", np.round(pad_mid("left"), 3).tolist(), "stock", in_container(zz_n, zz_cb), flush=True)
    for k_ in range(4):
        if in_container(zz_n, zz_cb)["lowest"] < 0.06:
            break
        r_ = thand("left", dz=-0.04, frame="world", Q={"left": q_(ts.ee_pose("left")[1])}, tag="stock_down")
        print("down", r_["grip_pt"], "stock", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "stock_low"), state(), flush=True)
