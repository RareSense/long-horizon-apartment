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
ROUTE[POS:] = [s_ for s_ in ROUTE[POS:] if item_name(s_) != "r196i1_plastic_bag"]      # given up, left lying in place (task list only)
print("RELOADED 3161 rec", rec.n, "route head", [item_name(s_) for s_ in ROUTE[POS:POS + 6]], flush=True)
for n_ in ("r196i1_plastic_bag", "r190i1_stocking", "r130i1_light_saber", "r120i2_duck", "r125i1_flat", "r175i1_cardboard_box", "r186i1_basket"):
    b_ = body_of(n_); lo_, hi_ = obj_box(b_); print(n_, np.round(centre(b_), 3).tolist(), "box", np.round(lo_[:2], 2).tolist(), np.round(hi_[:2], 2).tolist(), "dest", DESC["destinations"].get(n_), flush=True)
A_, ax_, a_, bid_, j_ = hinge_axis("r159i1_door"); print("tv door q", round(float(d.qpos[a_]), 3), "box", [np.round(v_, 2).tolist() for v_ in obj_box(m.body(bid_).name)], flush=True)
