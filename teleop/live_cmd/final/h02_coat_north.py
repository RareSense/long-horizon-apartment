print("ck", ck_save("bc_coat_held_right", kind="act"), flush=True)
# blanket held right: carry (arm frozen) to the corridor south of the scooter (-1.55,-1.17), facing east. AI-operated
zz_n = "r116i1_coat_pile"
CARRY_JOINTS = True
MON["trace"] = []
mon_start(target=None)
try:
    wk_ = None
    for g_ in ((-1.55, -1.17, 0.0), (-1.45, -1.17, 0.0), (-1.3, -1.2, 0.0), (-1.2, -1.2, 0.0)):
        try:
            wk_ = with_tight(lambda: walk_path(g_, ignore=(zz_n,), carry=("right",), tol=0.05)); print("goal", g_, flush=True); break
        except RuntimeError as ex_:
            print("no path", g_, str(ex_)[:80], flush=True)
    print("walk", {k_: (v_ if not isinstance(v_, (list, dict)) else str(v_)[:160]) for k_, v_ in (wk_ or {}).items()} if isinstance(wk_, dict) else wk_, flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("state", state(), "touch", contact_report(), "held", cloth_held("right"), "fell", fallen(), "scooter", np.round(centre(body_of("r126i1_scooter")), 3).tolist(), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), flush=True)
print("look3", look3("coat_corr"), flush=True)
# AI teleop: backward steps west along y -1.18 (facing east, blanket held ahead-right), then turn to face south at the
# north pre-stance (-2.148,-1.202). AI-operated
CARRY_JOINTS = True
log_ = []
for k_ in range(9):
    p_ = base()[0]
    if p_[0] < -2.13:
        break
    y_err = -1.19 - float(p_[1])
    tmove(fwd=-min(0.12, float(p_[0]) + 2.148), side=float(np.clip(y_err, -0.04, 0.04)), turn=float(np.clip(-np.degrees(base()[1]), -10, 10)), carry=("right",), tag=f"coat_bk{k_}")
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
    tmove(turn=float(np.clip(e_, -15, 15)), carry=("right",), tag=f"coat_tn{k_}")
    c_ = contact_report()
    log_.append(("turn", np.round(base()[0][:2], 3).tolist(), round(float(np.degrees(base()[1])), 1), c_["body"], c_["body_who"], cloth_held("right")))
for l_ in log_:
    print("MV", l_, flush=True)
print("END", state(), "held", cloth_held("right"), "fell", fallen(), "lowest", round(float(bc_w("r116i1_coat_pile").points(0)[:, 2].min()), 3), flush=True)
print("near", near_things(0.7), flush=True)
print(look3("coat_at_north_pre"), flush=True)
