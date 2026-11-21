mon_start(target=None); MON["ignore_names"] = (zz_cb,)
try:
    PRE_ACTION("unlock_grip", dict(side=SD)); unlock_grip(SD); open_jaws(SD, T=0.5); HELD.pop(SD, None); op.run(1.0)
    print("open", in_container(zz_n, zz_cb), flush=True)
    zQ = {SD: q_(ts.ee_pose(SD)[1])}
    for k_ in range(5):
        r_ = thand(SD, dz=0.04, frame="world", Q=zQ, tag="stock_up")
    print("up", in_container(zz_n, zz_cb), "fingers", finger_touch(SD), flush=True)
    r_ = thand(SD, dx=-0.04, tag="stock_back")
    PRE_ACTION("stand_up", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.4); rest_hands(SIDES, T=0.8); op.run(0.6)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
c_ = in_container(zz_n, zz_cb); print("stock", c_, "check", item_check(zz_n), "state", state(), "touch", contact_report()["body_who"], "fell", fallen(), flush=True)
print(look3("n1_stock_done"), flush=True)
