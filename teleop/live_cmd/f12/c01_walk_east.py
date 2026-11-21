mon_start(target=None)
try:
    _act("walk_path", goal=[3.30, -1.15, 180])
    w_ = walk_path((3.30, -1.15, np.pi))
    print("walk", {k_: v_ for k_, v_ in (w_ or {}).items() if k_ in ("ok", "err_xy", "err_yaw", "legs", "why")} if isinstance(w_, dict) else str(w_)[:300], flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print("umb", np.round(centre(body_of("r106i1_umbrella")), 3).tolist(), flush=True)
print(look3("f12_at_umb_east"), flush=True)
