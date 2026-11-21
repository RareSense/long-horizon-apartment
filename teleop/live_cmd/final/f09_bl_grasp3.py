zz_n = "r117i1_blanket"
P_ = bc_w(zz_n).points(0)
def _d4():
    g = room_grid((zz_n,))
    print("cost from here", round(float(g.reach_cost(base()[0][:2], np.array([0.91, -1.5]))), 2), flush=True)
with_tight(_d4)
MON["trace"] = []
zz_r = bigcloth_into(zz_n, s1="right", stop_after="grasp", uv=(-0.43, 0.0))
print("RESULT", [{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in zz_r], flush=True)
print("state", state(), "touch", contact_report(), "held R", cloth_held("right"), "fell", fallen(), "kit", kit_mem(), flush=True)
print("scooter", np.round(centre(body_of("r126i1_scooter")), 3).tolist(), flush=True)
print("look3", look3("blanket_grasped"), flush=True)
