mon_start(target=None); MON["ignore_names"] = (body_of("r130i1_light_saber"),); MON["start"].pop(zz_s, None)
try:
    for k_ in range(4):
        r_ = thand("left", dx=-0.04, tag="sc_left_back")
        print("left", r_["grip_pt"], "touch", contact_report()["body"], flush=True)
    rest_hands(SIDES, T=1.0); op.run(0.5)
    print("rested", state(), "touch", contact_report(), flush=True)
    r_ = tmove(fwd=-0.10, tag="sc_off")
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("scooter", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], "tilt", round(float(np.degrees(np.arccos(np.clip(obj_pos(zz_s)[1][2, 2], -1, 1)))), 1), "state", state(), "touch", contact_report(), flush=True)
print(look3("sc_free2"), flush=True)
