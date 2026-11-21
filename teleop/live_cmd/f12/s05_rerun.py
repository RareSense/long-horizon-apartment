MON["on"] = False
zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\0432_act_walk_via")
gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 3]], "done", len(DONE), "state", state(), flush=True)
print("scooter box", [np.round(v_, 3).tolist() for v_ in obj_box(body_of("r126i1_scooter"))], flush=True)
zz_r = park_scooter_hang("r126i1_scooter")
print("SCOOTER", {k_: v_ for k_, v_ in zz_r.items() if k_ not in ("moves",)}, flush=True)
if zz_r.get("status") == "done":
    zz_d = item_done_auto("r126i1_scooter", zz_r, spot=(-2.20, 0.0))
    print("DONE", zz_d, flush=True)
print("state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
