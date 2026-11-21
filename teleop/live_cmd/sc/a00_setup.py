# SCOUT (hall) session, AI-operated. Slot "cloth", port 47970. Side branch of the chain (NOT on the episode chain).
# Globals from the launcher: RUN_NEW (new run folder), CKP (start checkpoint).
ROOM = r"E:\urc_home\rooms\apartment_1122_full.json"; TASK = []; LIVE = True
RUN = RUN_NEW
import time as _tt; _t0 = _tt.time()
exec(open(r"E:\urc_home\scripts\home\episode.py", encoding="utf-8").read())
print("CPU", CPU, type(br).__name__, state(), "setup wall", round(_tt.time() - _t0, 1), flush=True)
for _f in ("route_v3_setup.py", "teleop.py", "autorun.py", "aside.py", "ops.py", "scooter.py"):
    exec(open(r"E:\urc_home\scripts\home\live\\" + _f, encoding="utf-8").read())
# gait_on / settle_after_load as in load_floor.py (its route_v3_resume is done here by hand: the 1071 gotcha)
_lf = open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read()
exec(_lf[_lf.index("GARMENTS_FIRST"):_lf.index("zz_m = route_v3_resume")])
zz_m = route_v3_resume(CKP)
print(gait_on())
# 1071 was saved 0.02 s after a lowering posture command began: cancel it at once, stay tall
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.4)); op.run(1.2)
print("tall", state(), "touch", contact_report(), flush=True)
exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f10\zz_put.py", encoding="utf-8").read())
import json as _json
_json.dump(dict(from_ckpt=CKP, room=ROOM, note="AI-operated. SCOUT (hall) run: duck r120, shoes r105, umbrella r107, towel r100 as one-call steps (side branch, NOT on the episode chain)."),
           open(os.path.join(RUN, "from_ckpt.json"), "w"), indent=1)
print("RUN", RUN, "SEG", SEG.get("from_ckpt"), flush=True)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 8]], "done", len(DONE), flush=True)
print("kit", kit_mem(), "state", state(), flush=True)
