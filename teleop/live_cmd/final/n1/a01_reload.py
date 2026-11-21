CK3161 = r"C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\checkpoints\3161_item_r125i2_flat_stand"
route_v3_resume(CK3161)
gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print('sync', ex_)
ATTEMPT = 0
exec(open(r'E:\urc_final\scripts\home\final_run\common_a.py', encoding='utf-8').read())
exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
exec(open(r'E:\urc_final\scripts\home\final_run\items_lib.py', encoding='utf-8').read())
print('RELOADED', rec.n, state(), 'route at', item_name(ROUTE[POS]) if POS < len(ROUTE) else None, 'done', len(DONE), flush=True)
P0 = base()[0]
for nm_ in ("r122i1_croc", "r125i2_flat", "r124i1_sandal", "r130i1_light_saber", "r126i1_scooter"):
    b_ = body_of(nm_); lo_, hi_ = obj_box(b_)
    print(nm_, "c", np.round(centre(b_), 3).tolist(), "box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), flush=True)
c_ = contact_report(); print("contacts", c_["body"], c_["body_who"], flush=True)
print("feet", {s_: np.round(d.xpos[m.body(s_ + "_ankle_roll_link").id], 3).tolist() for s_ in SIDES}, flush=True)
print(look3("n1_a01"), flush=True)
