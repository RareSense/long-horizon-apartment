ck_load(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok")
print(state(), "pos", POS, item_name(ROUTE[POS]))
# the knit hat's walk put a foot on the light saber r130 (22 N at (-1.03,-0.51)): the saber is set aside first, by the
# north wall (its basket corner is blocked), from the east where the robot now stands
zz_r = set_aside("r130i1_light_saber", (-1.9, 1.45), ignore=("r126i1_scooter",))
print("ASIDE", {k_: v_ for k_, v_ in zz_r.items() if k_ != "look"})
print("look", zz_r.get("look"), kit_mem())
if zz_r.get("status") == "done":
    zz_gr = go_item()
