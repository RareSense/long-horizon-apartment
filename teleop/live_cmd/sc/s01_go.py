exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
g_ = with_tight(lambda: room_grid(()))
print("free", [(x_, y_) for x_ in (2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5) for y_ in (-1.1, -1.2, -1.3, -1.4, -1.5, -1.6, -1.7) if g_.free(np.array([x_, y_]))], flush=True)
mon_start(target=None)
try:
    back_off_container(); w_ = walk_tight(SHOE_APPROACH); print("walk", w_.get("ok"), w_.get("err_xy"), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False; rest_hands(SIDES); op.run(1.0)
print("START", ck_save("shoe_approach", kind="start"), state(), flush=True)
for n_ in ("r105i1_shoe", "r105i2_shoe"):
    b_ = body_of(n_)
    for sd_ in ("left", "right"):
        try:
            st_, s2_, gp_ = pick_stance(b_, sd_); print(n_, sd_, "stance", np.round(st_, 3).tolist(), s2_, "gp", np.round(gp_["point"], 3).tolist(), "w", round(gp_["width"], 3), "closes", np.round(gp_["closes"][0], 2).tolist() if gp_["closes"] else None, "wall", gp_.get("wall"), flush=True)
        except Exception as ex_:
            print(n_, sd_, "ERR", str(ex_)[:120], flush=True)
print(look3("s01_at_shoes"), flush=True)
