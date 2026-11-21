ck_load(os.path.join(RUN, "checkpoints", "1632_item_r193i1_toy_piece")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
rec.still_every = 300
exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
print("RELOADED 1632 rec", rec.n, state(), flush=True)
pb_ = body_of("r149i1_pouch"); C_, c_, z0_, z1_ = flat_corners(pb_)
print("pouch", np.round(centre(pb_), 3).tolist(), "corners", np.round(C_, 3).tolist(), "z", round(z0_, 3), round(z1_, 3), flush=True)
for k_ in range(4):
    for sd_ in SIDES:
        print(k_, sd_, [dict(stance=np.round(p_["stance"], 3).tolist(), free=p_["free"]) for p_ in corner_pinch_plan(pb_, k_, sd_, 0.018)], flush=True)
