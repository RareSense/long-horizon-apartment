CHAIN = r"C:/Users/raresense/sim_home/runs/1120_093820_dex1_floor_12/checkpoints/2493_item_r158i1_tissue"
exec(open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read())
exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f10\zz_put.py", encoding="utf-8").read())
if "refresh_jointed_footprints" in globals():
    refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync_cloth", str(ex_)[:100], flush=True)
for f_ in ("u00_helpers.py", "basket_put.py", "cpick.py"):
    exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\\" + f_, encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\i02_surface.py", encoding="utf-8").read().split("ZZ = surf_item")[0])
CREEPERS.add(body_of("r100i1_towel"))
print("RUN", RUN, "route head", [item_name(s_) for s_ in ROUTE[POS:POS + 8]], "done", len(DONE), flush=True)
print("kit", kit_mem(), "state", state(), "hold_guard", "hold_guard" in globals(), "actions log", "_action_log" in globals(), flush=True)
