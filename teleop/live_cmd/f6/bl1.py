ck_load(os.path.join(RUN, "checkpoints", "0449_act_hand_move"))
gait_on(); op.run(0.3)
zz_w = GARMENTS["r117i1_blanket"]["w"]
zz_sd = "left"
print("at 0449", state(), "blanket", in_container("r117i1_blanket", zz_hb), "at_fingers", zz_w.at_fingers(zz_sd), "pad", np.round(pad_mid(zz_sd), 3).tolist(), "jaw", jaw_target.get(zz_sd), "HELD", list(HELD), "touch", contact_report(), flush=True)
print("look", look_hand(zz_sd, "bl_0449"), flush=True)
