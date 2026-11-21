ck_load(os.path.join(RUN, "checkpoints", "1632_item_r193i1_toy_piece")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
rec.still_every = 300
print("RELOADED 1632 rec", rec.n, state(), flush=True)
