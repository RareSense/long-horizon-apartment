ck_load(r"C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\checkpoints\3386_act_n1_off_croc"); gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
print("RELOADED 3386 at rec", rec.n, state(), flush=True)
_start_item("r196i1_plastic_bag")
zz_b = body_of("r196i1_plastic_bag")
mon_start(target=zz_b)
try:
    w_ = walk_tight((-4.807, -1.299, -0.435))
    print("walk", {k_: w_.get(k_) for k_ in ("ok", "err_xy")} if isinstance(w_, dict) else w_, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
bk_ = body_of("r186i1_basket"); print("basket box", [np.round(v_, 3).tolist() for v_ in obj_box(bk_)], flush=True)
if not fallen():
    print("ck", ck_save("n1_bag_stance", kind="act", info=dict(note="plastic bag corner-3 stance (AI-operated)")), flush=True)
print(look3("n1_b04"), flush=True)
