exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
b_ = body_of("r107i1_umbrella")
V_ = _hull_pts(b_); print("hull z", round(float(V_[:, 2].min()), 3), round(float(V_[:, 2].max()), 3), "axis", np.round(shoe_axis(b_)[0], 2).tolist(), "c", np.round(shoe_axis(b_)[1], 3).tolist(), flush=True)
gp_ = grasp_plan(b_)
for o_ in (gp_.get("options") or [gp_])[:6]:
    print("opt", np.round(o_["point"], 3).tolist(), "w", round(o_["width"], 3), "closes", np.round(o_["closes"][0], 2).tolist(), "score", round(o_.get("score", 0), 3), flush=True)
for sd_ in ("left", "right"):
    for tight_ in (False, True):
        try:
            r_ = (with_tight(lambda: pick_stance(b_, sd_)) if tight_ else pick_stance(b_, sd_))
            print(sd_, "tight" if tight_ else "normal", np.round(r_[0], 3).tolist(), np.round(r_[2]["point"], 3).tolist(), np.round(r_[2]["closes"][0], 2).tolist(), flush=True)
        except Exception as ex_:
            print(sd_, tight_, "ERR", str(ex_)[:100], flush=True)
g_ = with_tight(lambda: room_grid((b_,)))
rows_ = []
for y_ in np.arange(0.1, -1.31, -0.1):
    rows_.append(f"{y_:5.1f} " + "".join("." if g_.free(np.array([x_, y_])) else "#" for x_ in np.arange(0.0, 2.01, 0.1)))
print("x 0.0..2.0 step 0.1 (umbrella ignored)\n" + "\n".join(rows_), flush=True)
print(close(os.path.join(LK, "u01_umbrella.jpg"), np.r_[0.95, 0.2, 1.4], np.r_[0.95, -0.55, 0.0], "umbrella r107"), flush=True)
