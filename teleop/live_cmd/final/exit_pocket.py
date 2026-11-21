# out of the hamper pocket by teleop (AI-operated): face south, step to y -1.19, face east, east along y -1.19 to x -1.45
# (the planner sees no way out: scooter r126 north, rug toys west, hamper south).
log_ = []
def _mv(**kw):
    tmove(**kw)
    c_ = contact_report()
    log_.append((kw.get("tag"), np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"]))
    return c_["body"] < 3.0 and not fallen()
ok_ = True
if abs(-1.19 - float(base()[0][1])) >= 0.03:
    for k_ in range(8):
        e_ = float(np.degrees(wrapa(-np.pi / 2 - base()[1])))
        if abs(e_) < 4 or not ok_:
            break
        ok_ = _mv(turn=float(np.clip(e_, -15, 15)), tag=f"px_s{k_}")
    for k_ in range(4):
        dy_ = -1.19 - float(base()[0][1])
        if abs(dy_) < 0.03 or not ok_:
            break
        ok_ = _mv(fwd=float(np.clip(-dy_, -0.12, 0.12)), tag=f"px_y{k_}")
for k_ in range(8):
    e_ = float(np.degrees(wrapa(0.0 - base()[1])))
    if abs(e_) < 3 or not ok_:
        break
    ok_ = _mv(turn=float(np.clip(e_, -15, 15)), tag=f"px_e{k_}")
for k_ in range(9):
    p_ = base()[0]
    if p_[0] > -1.47 or not ok_:
        break
    ok_ = _mv(fwd=min(0.12, -1.45 - float(p_[0])), side=float(np.clip(-1.19 - float(p_[1]), -0.04, 0.04)), turn=float(np.clip(-np.degrees(base()[1]), -10, 10)), tag=f"px_east{k_}")
for l_ in log_:
    print("MV", l_, flush=True)
print("OUT", ok_, state(), flush=True)
