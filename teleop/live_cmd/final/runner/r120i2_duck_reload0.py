route_v3_resume(r'C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final\checkpoints\3161_item_r125i2_flat_stand')
gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print('sync', ex_)
print('RELOADED', rec.n, state(), 'route at', item_name(ROUTE[POS]) if POS < len(ROUTE) else None, flush=True)
