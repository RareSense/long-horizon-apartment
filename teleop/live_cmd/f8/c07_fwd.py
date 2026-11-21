mon_start(target=None); MON["ignore_names"] = (zz_cb,)
try:
    tpose(-0.19, 0.35, T=1.0, hands_side="left")
    print("lean", state()["pelvis"], "pad", np.round(pad_mid("left"), 3).tolist(), "stock", in_container(zz_n, zz_cb), flush=True)
    for k_ in range(3):
        r_ = thand("left", dx=0.04, frame="robot", Q={"left": q_(ts.ee_pose("left")[1])}, tag="stock_fwd")
        print("fwd", r_["grip_pt"], r_["err"], "stock", in_container(zz_n, zz_cb), "touch", contact_report()["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "stock_fwd_end"), state(), flush=True)
