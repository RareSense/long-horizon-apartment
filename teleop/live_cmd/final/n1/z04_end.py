route_v3_resume(os.path.join(RUN, "checkpoints", "0270_item_r83i1_sponges")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
print("CHAIN END reloaded rec", rec.n, "done", len(DONE), "route left", [item_name(s_) for s_ in ROUTE[POS:]], state(), flush=True)
