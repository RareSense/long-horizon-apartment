mon_start(target=None); MON["ignore_names"] = (zz_cb,)
try:
    PRE_ACTION("unlock_grip", dict(side="left"))
    unlock_grip("left"); open_jaws("left", T=0.5); HELD.pop("left", None); op.run(0.6)
    print("open", "stock", in_container(zz_n, zz_cb), flush=True)
    for k_ in range(5):
        r_ = thand("left", dz=0.04, frame="world", Q={"left": q_(ts.ee_pose("left")[1])}, tag="stock_up")
        print("up", r_["grip_pt"], "stock", in_container(zz_n, zz_cb), "fingers", finger_touch("left"), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look_hand("left", "stock_released"), state(), flush=True)
