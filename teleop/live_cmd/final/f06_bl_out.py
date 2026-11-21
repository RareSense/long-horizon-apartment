zz_n = "r117i1_blanket"
print("near", near_things(0.8), flush=True)
ok_, log_ = step_to([(-2.01, -0.72)], fwd_max=0.12, tols=[0.06])
print("STEP_TO", ok_, log_[-3:], state(), "touch", contact_report(), "fell", fallen(), flush=True)
print(look3("bl_out"), flush=True)
if ok_ and not fallen():
    MON["trace"] = []
    zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(-0.43, 0.0))
    print("RESULT", [{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in zz_r], flush=True)
    print("state", state(), "touch", contact_report(), "held R", cloth_held("right"), "kit", kit_mem(), flush=True)
    print("look3", look3("blanket_grasped"), flush=True)
