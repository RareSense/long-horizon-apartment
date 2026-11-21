import time as _tm
MON["on"] = False
_w0 = _tm.time()
mon_start(target=None)
try:
    w_ = walk_tight((1.95, -1.10, -1.571))
    print("walk", {k_: v_ for k_, v_ in w_.items() if k_ in ("ok", "err_xy", "err_yaw", "legs", "why")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
rest_hands(SIDES); op.run(0.5)
print("state", state(), "fell", fallen(), "wall", round(_tm.time() - _w0), flush=True)
print(look3("d01_at_duck_approach"), flush=True)
b_ = body_of("r120i1_duck")
print("duck", np.round(centre(b_), 3).tolist(), "gp", {k_: (np.round(v_, 3).tolist() if hasattr(v_, "tolist") else v_) for k_, v_ in (grasp_plan(b_) or {}).items() if k_ in ("point", "z", "top", "closes", "width", "wall", "at")}, flush=True)
