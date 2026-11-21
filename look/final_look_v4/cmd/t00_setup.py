# FINAL LOOK test session (AI-operated). The apartment at chain checkpoint 2493 (tissue) with the final look of branch
# final-look (E:\urc_look: boot.py + cloth_skills.py hooks, src/urc/tasks/home/final_look.py). Render check only: no
# task is run; the robot only stands after the standard checkpoint load.
import os, time as _tt
_t0 = _tt.time()
os.environ["URC_TEXTURED"] = "1"; os.environ["URC_ROUGH_FLOOR"] = "0.8"; os.environ.pop("URC_FINAL_LOOK", None)
ROOM = r"E:\urc_home\rooms\apartment_1122_full.json"; TASK = []; LIVE = True
RUN = r"C:\Users\raresense\sim_home\apartment\final_look_v4\run_AI_operated"
CKP = r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\2493_item_r158i1_tissue"
_ep = open(r"E:\urc_look\scripts\home\episode.py", encoding="utf-8").read()
_ep = _ep.replace(r"E:\urc_home\scripts\home\boot.py", r"E:\urc_look\scripts\home\boot.py").replace(
    r"E:\urc_home\scripts\home\cloth_skills.py", r"E:\urc_look\scripts\home\cloth_skills.py")
exec(_ep)
print("FINAL_LOOK", FINAL_LOOK, flush=True)
for _f in ("route_v3_setup.py", "teleop.py", "autorun.py", "aside.py", "ops.py", "scooter.py"):
    exec(open(r"E:\urc_home\scripts\home\live\\" + _f, encoding="utf-8").read())
_lf = open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read()
exec(_lf[_lf.index("GARMENTS_FIRST"):_lf.index("zz_m = route_v3_resume")])
zz_m = route_v3_resume(CKP); print(gait_on()); sync_cloth(force=True)
refresh_jointed_footprints(); rest_hands(SIDES)
op.run(4.0, until=_standing); op.run(1.5)
print("LOADED", CKP, state(), "kit", kit_mem(), "wall", round(_tt.time() - _t0, 1), flush=True)
