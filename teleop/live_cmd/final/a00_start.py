# FINAL clean recorded episode, STEP 1 (AI-operated): episode start state + removal of the 26 things at frame 0.
# Code: E:\urc_final (branch final-episode). Start = seg3's episode start checkpoint (the first chain began there).
START = r"C:\Users\raresense\sim_home\runs\1119_152622_route_v3_seg3\checkpoints\0000_item_start"
CHAIN_END_META = r"C:\Users\raresense\sim_home\runs\1120_155109_dex1_floor_14\checkpoints\0557_item_r83i1_sponges\meta.json"
import json as _json_f
for _f in ("route_v3_setup.py", "teleop.py", "autorun.py", "aside.py", "ops.py", "scooter.py"):
    exec(open(r"E:\urc_final\scripts\home\live\\" + _f, encoding="utf-8").read())
_lf = open(r"E:\urc_final\scripts\home\live\load_floor.py", encoding="utf-8").read()
exec(_lf.split("zz_m = route_v3_resume(CHAIN)")[0].split("\n", 2)[2])     # GARMENTS_FIRST, gait_on, settle_after_load
zz_m = route_v3_resume(START)
print(gait_on(), flush=True)
# frame 0: the 26 removed things off-map (REMOVED_FOR_40.json: removed_sink_bound + removed_hard + removed_final)
_rj = _json_f.load(open(r"C:\Users\raresense\sim_home\apartment\REMOVED_FOR_40.json", encoding="utf-8"))
RM_NAMES = _rj["removed_sink_bound"] + _rj["removed_hard"] + _rj["removed_final"]
RM_OUT = {}
for _n in RM_NAMES:
    try:
        RM_OUT.update(remove_bodies([_n], origin=(25.0 + 1.5 * (len(RM_OUT) % 6), 25.0 + 1.5 * (len(RM_OUT) // 6))))
    except Exception as _ex:
        print("REMOVE FAILED", _n, str(_ex)[:200], flush=True)
print("removed", len(RM_OUT), "of", len(RM_NAMES), flush=True)
# the route: the 36 items in the first chain's order (its chain-end route, first 36 steps)
_cm = _json_f.load(open(CHAIN_END_META, encoding="utf-8"))
ROUTE[:] = [list(s_) for s_ in _cm["info"]["route"]["route"][:36]]
POS = 0; DONE.clear(); SKIPPED.clear()
apply_ovr()
print("ROUTE", len(ROUTE), [item_name(s_) for s_ in ROUTE], flush=True)
exec(open(r"E:\urc_final\scripts\home\live\bigcloth.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f10\zz_put.py", encoding="utf-8").read())
for _f in (r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\u00_helpers.py", r"E:\urc_final\scripts\home\live\basket_put.py", r"E:\urc_final\scripts\home\live\cpick.py"):
    exec(open(_f, encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\i02_surface.py", encoding="utf-8").read().split("ZZ = surf_item")[0])
settle_after_load()
rest_hands(SIDES); op.run(1.0)
print("RUN", RUN, "kit", kit_mem(), "state", state(), "hold_guard", "hold_guard" in globals(), "actions log", "_action_log" in globals(), flush=True)
print("srec", getattr(globals().get("rec"), "srec", "no srec yet"), flush=True)
