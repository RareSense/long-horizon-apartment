for zz_c in ("0004_act_walk", "0005_act__turn_on_spot", "0007_act_sc_hands_to", "0010_act_sc_hands_to", "0013_act_sc_close"):
    ck_load(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\\" + zz_c)
    print(zz_c, state())
