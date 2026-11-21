# FINAL LOOK v4 (AI-operated, render only): FRESH boot of the frozen apartment at the episode START state: no checkpoint
# is loaded, every original mess item where the room file puts it (garments laid as cloth by the boot), the robot at its
# start pose. The renderer is set to PathTracing BEFORE the boot so this session never allocates the RT pipeline.
import os, time as _tt, carb
_t0 = _tt.time()
carb.settings.get_settings().set("/rtx/rendermode", "PathTracing")
carb.settings.get_settings().set("/rtx/pathtracing/spp", 1); carb.settings.get_settings().set("/rtx/pathtracing/totalSpp", 1)
os.environ["URC_TEXTURED"] = "1"; os.environ["URC_ROUGH_FLOOR"] = "0.8"; os.environ.pop("URC_FINAL_LOOK", None)
ROOM = r"E:\urc_home\rooms\apartment_1122_full.json"; TASK = []; LIVE = True
RUN = r"C:\Users\raresense\sim_home\apartment\final_look_v4\run_AI_operated_start"
_ep = open(r"E:\urc_look\scripts\home\episode.py", encoding="utf-8").read()
_ep = _ep.replace(r"E:\urc_home\scripts\home\boot.py", r"E:\urc_look\scripts\home\boot.py").replace(
    r"E:\urc_home\scripts\home\cloth_skills.py", r"E:\urc_look\scripts\home\cloth_skills.py")
_ep = _ep.replace('views_enable(("room", "head")); warm_up(40)', 'views_enable(("room",)); warm_up(40)')   # no head view render product (memory)
exec(_ep)
exec(open(r"E:\urc_home\scripts\home\live\ops.py", encoding="utf-8").read())      # kit_mem()
print("FINAL_LOOK", FINAL_LOOK, flush=True)
print("START_LOADED (no checkpoint)", state(), "kit", kit_mem(), "wall", round(_tt.time() - _t0, 1), flush=True)
