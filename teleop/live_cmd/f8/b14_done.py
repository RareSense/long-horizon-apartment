mon_start(target=None); MON["ignore_names"] = (zz_bin, zz_b)
try:
    for k_ in range(3):
        r_ = thand("left", dx=-0.04, dz=0.0, tag="hand_back")
    rest_hands(("left",), T=0.8); op.run(0.5)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "touch", contact_report(), "bag inside", inside(zz_b, zz_bin), "route at", item_name(ROUTE[POS]), flush=True)
print(look3("bag_done"), flush=True)
