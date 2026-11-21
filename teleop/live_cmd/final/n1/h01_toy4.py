ck_load(os.path.join(RUN, "checkpoints", "0986_item_r179i1_toy_pouch")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
rec.still_every = 300
exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n1\rug_lib.py", encoding="utf-8").read())
print("RELOADED 0986 rec", rec.n, state(), flush=True)
print("ZZ_OK", rug_toy("r193i4_toy_piece", "left"), "done", len(DONE), "rec", rec.n, flush=True)
