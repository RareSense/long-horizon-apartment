MON["on"] = False
zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\1077_act_surface_posture")
gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(0.5)
print("loaded", state(), "touch", contact_report()["body"], "route", [item_name(s_) for s_ in ROUTE[POS:POS + 4]], flush=True)
ZZ = surf_item("r93i1_nugget")
print("in basket", inside(body_of("r93i1_nugget"), body_of("r186i1_basket")), flush=True)
