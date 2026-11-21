TWO["on"] = False
ck_load(r"C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints\0035_act_n1_bag_north_stance"); gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
print("RELOADED 0035 rec", rec.n, flush=True)
zz_b = body_of("r196i1_plastic_bag")
mon_start(target=zz_b)
try:
    w_ = walk_tight((-4.807, -1.299, -0.435))
    print("walk", {k_: w_.get(k_) for k_ in ("ok", "err_xy")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "touch", contact_report()["body_who"], "bag", np.round(centre(zz_b), 3).tolist(), "rec", rec.n, flush=True)
if not fallen():
    print("ck", ck_save("n1_bag_k3_stance", kind="act", info=dict(note="plastic bag corner-3 stance (AI-operated)")), flush=True)
