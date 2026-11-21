ck_load(r"C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints\0170_act_n1_start_bag_kept"); gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
print("RELOADED 0170 rec", rec.n, state(), "route", item_name(ROUTE[POS]), flush=True)
_start_item("r190i1_stocking")
mon_start(target=None)
try:
    w_ = walk_tight((-1.45, -1.19, np.pi))
    print("walk", {k_: w_.get(k_) for k_ in ("ok", "err_xy", "way_points")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print(look3("n1_c06"), flush=True)
