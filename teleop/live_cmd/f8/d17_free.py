mon_start(target=None); MON["ignore_names"] = (body_of("r130i1_light_saber"),)
MON["start"].pop(zz_s, None)
try:
    for s_ in SIDES:
        thand(s_, dz=0.04, frame="world", tag="sc_free_up"); thand(s_, dz=0.03, frame="world", tag="sc_free_up")
    print("up touch", contact_report(), flush=True)
    for s_ in SIDES:
        thand(s_, dx=-0.04, tag="sc_free_back"); thand(s_, dx=-0.04, tag="sc_free_back")
    rest_hands(SIDES, T=0.8); op.run(0.4)
    r_ = tmove(fwd=-0.10, tag="sc_off")
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("scooter", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], "tilt", round(float(np.degrees(np.arccos(np.clip(obj_pos(zz_s)[1][2, 2], -1, 1)))), 1), "state", state(), "touch", contact_report(), flush=True)
print(look3("sc_free"), flush=True)
