mon_start(target=None); MON["ignore_names"] = (zz_cb,)
try:
    r_ = thand("left", dz=0.04, frame="world", tag="stock_up2"); r_ = thand("left", dx=-0.04, tag="stock_back")
    PRE_ACTION("stand_up", {}); stand_up(); rest_hands(SIDES, T=0.8); op.run(0.6)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("stock", in_container(zz_n, zz_cb), "state", state(), "touch", contact_report(), "fell", fallen(), flush=True)
print(look3("stock_done"), flush=True)
