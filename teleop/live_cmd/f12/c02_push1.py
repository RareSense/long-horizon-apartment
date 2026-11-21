exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\slab.py", encoding="utf-8").read())
mon_start(target=None)
try:
    w_ = walk_tight((3.10, -0.97, np.pi))
    print("walk", {k_: v_ for k_, v_ in (w_ or {}).items() if k_ in ("ok", "err_xy", "err_yaw")} if isinstance(w_, dict) else str(w_)[:300], flush=True)
except Abort as ex_:
    print("ABORT walk", str(ex_)[:300], flush=True)
MON["on"] = False
print("state", state(), flush=True)
r_ = slab_push("left", (-1.0, 0.0), (3.0, -1.20))
print("PUSH", r_, flush=True)
print(look3("f12_push1"), flush=True)
print(close(os.path.join(TELE_DIR, "f12_push1_top.jpg"), np.array([2.6, -0.9, 2.2]), np.array([2.3, -1.2, 0.0]), "push1 top"), flush=True)
