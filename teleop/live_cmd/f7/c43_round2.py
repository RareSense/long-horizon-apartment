ck_load(os.path.join(RUN, "checkpoints", "0994_act_toy_corner_basket_pre_ok")); gait_on(); settle_after_load()
exec(open(r"E:\urc_home\scripts\home\basket_skills.py", encoding="utf-8").read())
print("loaded", state(), "CARRY_Z", CARRY_Z, "BASKET_CARRY_Z", BASKET_CARRY_Z, "done", len(DONE), flush=True)
zz_names = ["r120i2_duck", "r192i1_ball", "r193i1_toy_piece", "r193i3_toy_piece", "r193i4_toy_piece", "r193i2_toy_piece", "r191i1_toy_vehicle"]
print(floor_first(zz_names)[:8], flush=True)
MON["trace"] = []
zz_r = with_tight(lambda: run_basket_round(zz_names))
print("ROUND", str({k_: v_ for k_, v_ in zz_r.items() if k_ != "look"})[:1800], flush=True)
print("state", state(), "fell", fallen(), "touch", contact_report(), "done", len(DONE), "kit", kit_mem(), flush=True)
print("look", look3("basket_round_end2"), flush=True)
