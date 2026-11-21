import sys
zz_goal = float(globals().get("ZZ_GOAL_YAW", 40.0)); zz_n_max = int(globals().get("ZZ_NMAX", 3))
zz_log = []
try:
    for k_ in range(zz_n_max):
        e_ = float(np.degrees(wrapa(np.radians(zz_goal) - base()[1])))
        if abs(e_) < 3.0: break
        zz_log.append(zz_pivot_step(zz_s, float(np.clip(e_, -5.0, 5.0)), "sc_pivot")); print(zz_log[-1], flush=True)
        zz_log.append(zz_regrip(zz_s, "regrip")); print(zz_log[-1], flush=True)
except Abort as ex_:
    zz_log.append(("abort", str(ex_)))
    print("ABORT", ex_, flush=True)
print("state", state(), "touch", contact_report(), "scooter box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_s)], "kit", kit_mem(), flush=True)
print(look3("sc_turns"), flush=True)
