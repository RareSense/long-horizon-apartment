mon_start(target=None); MON["ignore_names"] = (zz_cb,)
try:
    for k_ in range(3):
        r_ = thand("left", dz=-0.04, frame="world", Q={"left": q_(ts.ee_pose("left")[1])}, tag="stock_down2")
        print("down", r_["grip_pt"], r_["err"], "stock", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "stock_down2_end"), state(), flush=True)
