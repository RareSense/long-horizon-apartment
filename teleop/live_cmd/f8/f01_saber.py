print("ck", ck_save("scooter_moved_west_saber_free", kind="act", info=dict(note="scooter r126 taken, backed 0.25 m west, 3 pivot steps about its far wheel with re-grips, set down upright at x -2.43..-1.78; robot stepped off; route = 0512 chain end")), flush=True)
print(floor_first(["r130i1_light_saber"])[:3], flush=True)
zz_sb = body_of("r130i1_light_saber")
print("saber grasp", str(grasp_plan(zz_sb))[:400], flush=True)
MON["trace"] = []; MON["t_max"] = 900.0
globals()["CARRY_JOINTS"] = True
try:
    zz_o = zz_pick_put("r130i1_light_saber", (-4.92, -1.405))
finally:
    globals()["CARRY_JOINTS"] = False
print("OUT", str(zz_o)[:1500], flush=True)
print("state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
