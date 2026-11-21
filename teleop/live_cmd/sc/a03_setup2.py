# SCOUT session 2 (fresh after the 15:00 memory squeeze), AI-operated. Globals from the launcher: RUN_NEW, CKP.
ROOM = r"E:\urc_home\rooms\apartment_1122_full.json"; TASK = []; LIVE = True
RUN = RUN_NEW
exec(open(r"E:\urc_home\scripts\home\episode.py", encoding="utf-8").read())
for _f in ("route_v3_setup.py", "teleop.py", "autorun.py", "aside.py", "ops.py", "scooter.py"):
    exec(open(r"E:\urc_home\scripts\home\live\\" + _f, encoding="utf-8").read())
_lf = open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read()
exec(_lf[_lf.index("GARMENTS_FIRST"):_lf.index("zz_m = route_v3_resume")])
exec(open(r"E:\urc_home\scripts\home\live\bigcloth.py", encoding="utf-8").read())
exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
LK = os.path.join(RUN, "look"); os.makedirs(LK, exist_ok=True)
LD = CKP; exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\sc\ld.py", encoding="utf-8").read())
import json as _json
_json.dump(dict(from_ckpt=CKP, room=ROOM, note="AI-operated. SCOUT (hall) session 2: umbrella r107, towel r100 one-call steps (side branch, NOT on the episode chain)."), open(os.path.join(RUN, "from_ckpt.json"), "w"), indent=1)
print("RUN", RUN, "kit", kit_mem(), flush=True)
