route_v3_resume(r'C:\Users\raresense\sim_home\runs\1121_034845_dex1_floor_final_s3\checkpoints\0167_item_r125i1_flat')
gait_on(); settle_after_load()
if 'refresh_jointed_footprints' in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print('sync', ex_)
print('RELOADED', rec.n, state(), 'route at', item_name(ROUTE[POS]) if POS < len(ROUTE) else None, flush=True)
