if "refresh_jointed_footprints" in globals():
    print("jointed", refresh_jointed_footprints(), flush=True)
zz_xgoal = float(globals().get("ZZ_XW", 0.29)); zz_n = int(globals().get("ZZ_N", 6))
zz_log = []
try:
    for k_ in range(zz_n):
        st_ = zz_sc_state(zz_s)
        if st_["W"][0] >= zz_xgoal - 0.02: break
        if max(st_["pads"].values()) > 0.022:
            zz_log.append(("regrip", zz_regrip(zz_s, "push_regrip")))
        step_ = float(min(0.12, zz_xgoal - st_["W"][0] + 0.02))
        tr_ = float(np.clip(-(st_["yaw"] - st_["deck"]) * 0.5, -4, 4))
        zz_log.append(zz_fwd_step(zz_s, step_, "sc_push") if abs(tr_) < 1.0 else (lambda r_: r_)(tmove(carry=tuple(SIDES), fwd=step_, turn=tr_, tag="sc_push")))
        print(k_, zz_sc_state(zz_s), "touch", contact_report()["body"], flush=True)
        if MON.get("why"): raise Abort(MON["why"])
except Abort as ex_:
    print("ABORT", ex_, flush=True)
print("SC", zz_sc_state(zz_s), "state", state(), "touch", contact_report(), "kit", kit_mem(), flush=True)
print(look3("sc_push"), flush=True)
