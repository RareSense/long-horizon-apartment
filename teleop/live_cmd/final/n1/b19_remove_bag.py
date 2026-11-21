TWO["on"] = False
route_v3_resume(r"C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\checkpoints\3161_item_r125i2_flat_stand")
gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print('sync', ex_)
print("RELOADED 3161 rec", rec.n, state(), flush=True)
zz_b = body_of("r196i1_plastic_bag"); print("bag before", np.round(centre(zz_b), 3).tolist(), flush=True)
PRE_ACTION("remove_bodies", dict(names=["r196i1_plastic_bag"], why="last resort: 10 g flat board, no honest grasp after 6 real tries (corner pinch ejects it, two-hand paddles ride over it, pin+pinch tipped)"))
print("removed", remove_bodies(["r196i1_plastic_bag"]), flush=True)
op.run(1.0)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 6]], "done", len(DONE), flush=True)
print("ck", ck_save("n1_removed_plastic_bag", kind="act", info=dict(note="plastic bag r196 removed from the scene (REMOVED_FOR_40.json removed_final); AI-operated", removed=["r196i1_plastic_bag"])), "rec", rec.n, flush=True)
