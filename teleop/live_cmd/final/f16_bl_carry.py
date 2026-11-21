zz_n = "r117i1_blanket"
BC["stage"] = "grasp"
print("ck", ck_save("bc_blanket_held_right", kind="act"), flush=True)
MON["trace"] = []
zz_r = bigcloth_into(zz_n, s1="right", start="carry", stop_after="carry")
print("RESULT", [{k_: v_ for k_, v_ in r_.items() if k_ != "look"} for r_ in zz_r], flush=True)
print("state", state(), "touch", contact_report(), "held R", cloth_held("right"), "fell", fallen(), "lowest", round(float(bc_w(zz_n).points(0)[:, 2].min()), 3), flush=True)
print("scooter", np.round(centre(body_of("r126i1_scooter")), 3).tolist(), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), flush=True)
print("look3", look3("bl_carried"), flush=True)
