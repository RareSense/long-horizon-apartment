exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\zz_grasp.py", encoding="utf-8").read())
zz_ip = 136; zz_sd = "right"
zz_goal = with_tight(lambda: stance_for(np.r_[zz_w().points(0)[zz_ip][:2], 0.0], zz_sd, X_REL, Y_REL, ignore=(zz_BL,), squat=True, clear_of=(garment_rect(zz_BL),)))
print("goal", np.round(zz_goal, 3).tolist(), flush=True)
rest_hands((zz_sd,), T=0.3)
zz_wk = zz_walk_stance(zz_goal)
print("walk", {k_: (v_ if not isinstance(v_, (list, dict)) or k_ in ("goal", "base", "abort") else str(v_)[:200]) for k_, v_ in (zz_wk or {}).items()}, flush=True)
print(state(), contact_report(), "in_reach", in_reach(zz_w().points(0)[zz_ip], zz_sd), "mon", MON.get("why"), flush=True)
print("look", look3("at_blanket_stance"), flush=True)
