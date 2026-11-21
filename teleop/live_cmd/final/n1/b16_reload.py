TWO["on"] = False
ck_load(r"C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints\0035_act_n1_bag_north_stance"); gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
print("RELOADED 0035 rec", rec.n, state(), flush=True)
