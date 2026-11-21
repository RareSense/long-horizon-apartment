# blanket r117i1 with the bigcloth skill (Fable's hand-over-hand as stages), stage by stage. AI-operated
zz_n = "r117i1_blanket"
CK_STATE["item"] = f"{POS + 1:03d}_{zz_n}"
MON["trace"] = []
zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(-0.43, 0.0))
print("RESULT", [{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in zz_r], flush=True)
print("state", state(), "touch", contact_report(), "held R", cloth_held("right"), "kit", kit_mem(), flush=True)
print("look3", look3("blanket_grasped"), flush=True)
