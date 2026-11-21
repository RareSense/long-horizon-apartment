MON["ignore_names"] = tuple(set(MON.get("ignore_names", ())) | {zz_s, body_of("r130i1_light_saber")})
try:
    PRE_ACTION("sc_set_down", {}); print("down", sc_set_down(zz_s, speed=0.03, max_dz=0.05), flush=True)
    PRE_ACTION("sc_release", {}); MON["held"] = {}
    for s_ in SIDES: ts.ctrl.ext.pop(f"hold_{s_}", None)
    sc_release(zz_s); op.run(0.5)
    r_ = tmove(fwd=-0.10, tag="sc_off")
    print("off", r_["at"], r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
sp_ = scooter_parts(zz_s)
print("scooter", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], "tilt", round(float(np.degrees(np.arccos(np.clip(obj_pos(zz_s)[1][2, 2], -1, 1)))), 1), "deck", np.round(sp_["deck"], 3).tolist(), "state", state(), "touch", contact_report(), flush=True)
print(look3("sc_parked_temp"), flush=True)
