# coat pile r116i1 (AI-operated): out of the hamper pocket by teleop (north 2 x back, face east, east along y -1.19),
# then the bigcloth skill: grasp uv (0, 0.30) right (as the first chain), stop after the grasp.
zz_n = "r116i1_coat_pile"
CK_STATE["item"] = f"{POS + 1:03d}_{zz_n}"
log_ = []
def _mv(**kw):
    tmove(**kw)
    c_ = contact_report()
    log_.append((kw, np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"]))
    return c_["body"] < 3.0 and not fallen()
ok_ = True
for k_ in range(3):
    if base()[0][1] > -1.22 or not ok_:
        break
    ok_ = _mv(fwd=-min(0.12, -1.19 - float(base()[0][1]) + 0.0 if False else 0.12), tag=f"coat_back{k_}")
for k_ in range(7):
    e_ = float(np.degrees(wrapa(0.0 - base()[1])))
    if abs(e_) < 3 or not ok_:
        break
    ok_ = _mv(turn=float(np.clip(e_, -15, 15)), tag=f"coat_turn{k_}")
for k_ in range(9):
    p_ = base()[0]
    if p_[0] > -1.47 or not ok_:
        break
    ok_ = _mv(fwd=min(0.12, -1.45 - float(p_[0])), side=float(np.clip(-1.19 - float(p_[1]), -0.04, 0.04)), turn=float(np.clip(-np.degrees(base()[1]), -10, 10)), tag=f"coat_east{k_}")
for l_ in log_:
    print("MV", l_, flush=True)
print("OUT", ok_, state(), flush=True)
if ok_:
    MON["trace"] = []
    zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(0.0, 0.30))
    print("RESULT", [{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in zz_r], flush=True)
    print("state", state(), "touch", contact_report(), "held R", cloth_held("right"), "fell", fallen(), "coat box", [np.round(v_, 3).tolist() for v_ in garment_box(zz_n)], flush=True)
print("look3", look3("coat_grasped"), flush=True)
