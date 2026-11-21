mon_start(target=None); MON["ignore_names"] = (body_of("r130i1_light_saber"), zz_s); MON["start"].pop(zz_s, None)
try:
    for k_ in range(2):
        r_ = tmove(fwd=-0.12, tag="sc_off")
        print("off", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("scooter", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], "tilt", round(float(np.degrees(np.arccos(np.clip(obj_pos(zz_s)[1][2, 2], -1, 1)))), 1), "state", state(), "touch", contact_report(), "fell", fallen(), flush=True)
print(look3("sc_free3"), flush=True)
