# Live tuning v4 (AI-operated, render only): reloads urc.tasks.home.final_look, applies pack_pbr, cabinet_wood,
# prop_looks, surface_wear, daylight again (idempotent), then PT stills (p10_pt.py). Globals: SHOTS_, OUTD_, SPP_, ISO_.
import importlib, importlib.util, glob as _gl, urc.tasks.home.final_look as FL
for _p in _gl.glob(r"C:\Users\raresense\sim_home\_cloth\_pyc_live\**\final_look*.pyc", recursive=True):
    try: os.remove(_p)
    except OSError: pass
try: os.remove(importlib.util.cache_from_source(FL.__file__))
except OSError: pass
importlib.reload(FL)
_lg = lambda s: print(s[:600])
if globals().get("REAPPLY_", True):
    FL.pack_pbr(stage, log=_lg); FL.cabinet_wood(stage, SCN["top"], log=_lg); FL.prop_looks(stage, SCN["top"], log=_lg)
    FL.surface_wear(stage, log=_lg); FL.daylight(stage, FL.TL.USD_MAP, SCN["top"], log=_lg); FL.garment_looks(stage, GARMENTS, log=_lg)
exec(open(r"C:\Users\raresense\sim_home\apartment\final_look_v4\cmd\p10_pt.py", encoding="utf-8").read())
