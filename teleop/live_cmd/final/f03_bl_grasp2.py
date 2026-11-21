zz_n = "r117i1_blanket"
mon_start(target=None)
try:
    print("back_off", back_off_container(), flush=True)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("after backoff", state(), contact_report(), flush=True)
P_ = bc_w(zz_n).points(0)
try:
    g_ = with_tight(lambda: stance_for(np.r_[P_[136][:2], 0.0], "right", X_REL, Y_REL, ignore=(zz_n,), squat=True, clear_of=()))
    print("stance now", np.round(g_, 3).tolist(), flush=True)
except Exception as ex_:
    print("stance ERR", str(ex_)[:160], flush=True)
    g_ = None
if g_ is not None:
    MON["trace"] = []
    zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(-0.43, 0.0))
    print("RESULT", [{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in zz_r], flush=True)
print("state", state(), "touch", contact_report(), "held R", cloth_held("right"), "kit", kit_mem(), flush=True)
print("look3", look3("blanket_grasped"), flush=True)
