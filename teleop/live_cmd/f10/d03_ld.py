ck_load(os.path.join(RUN, "checkpoints", "0232_act_walk_to_stance")); gait_on(); settle_after_load(); refresh_jointed_footprints()
zz_b = body_of("r178i1_ball")
print("state", state(), "ball rel", np.round(rel(centre(zz_b)), 3).tolist(), "ball", np.round(centre(zz_b), 3).tolist(), flush=True)
print(look3("ball_ld"), flush=True)
