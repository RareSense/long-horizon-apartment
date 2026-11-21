exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
b_ = body_of("r120i1_duck")
gp_ = duck_head_plan(b_); print("head plan", {k_: (np.round(v_, 3).tolist() if hasattr(v_, "tolist") else v_) for k_, v_ in gp_.items() if k_ != "closes"}, flush=True)
GP_FORCE[b_] = duck_head_plan
try:
    zs_ = pick_stance(b_, "auto"); print("stance", np.round(zs_[0], 3).tolist(), zs_[1], np.round(zs_[2]["closes"][0], 2).tolist(), flush=True)
except Exception as ex_:
    print("stance err", ex_, "tight:", flush=True)
    zs_ = with_tight(lambda: pick_stance(b_, "auto")); print("tight stance", np.round(zs_[0], 3).tolist(), zs_[1], np.round(zs_[2]["closes"][0], 2).tolist(), flush=True)
GP_FORCE.pop(b_, None)
