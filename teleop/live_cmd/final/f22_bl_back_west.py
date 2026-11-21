# AI teleop: backward steps west along y -1.18 (facing east, blanket held ahead-right), then turn to face south at the
# north pre-stance (-2.148,-1.202). AI-operated
CARRY_JOINTS = True
log_ = []
for k_ in range(9):
    p_ = base()[0]
    if p_[0] < -2.13:
        break
    y_err = -1.19 - float(p_[1])
    tmove(fwd=-min(0.12, float(p_[0]) + 2.148), side=float(np.clip(y_err, -0.04, 0.04)), turn=float(np.clip(-np.degrees(base()[1]), -10, 10)), carry=("right",), tag=f"bl_back{k_}")
    c_ = contact_report()
    log_.append(("back", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"], cloth_held("right")))
    if c_["body"] > 3.0 or fallen() or not cloth_held("right"):
        break
for k_ in range(7):
    if c_["body"] > 3.0 or fallen():
        break
    e_ = float(np.degrees(wrapa(-np.pi / 2 - base()[1])))
    if abs(e_) < 3:
        break
    tmove(turn=float(np.clip(e_, -15, 15)), carry=("right",), tag=f"bl_turn{k_}")
    c_ = contact_report()
    log_.append(("turn", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"], cloth_held("right")))
for l_ in log_:
    print("MV", l_, flush=True)
print("END", state(), "held", cloth_held("right"), "fell", fallen(), "lowest", round(float(bc_w("r117i1_blanket").points(0)[:, 2].min()), 3), flush=True)
print("near", near_things(0.7), flush=True)
print(look3("bl_at_north_pre"), flush=True)
