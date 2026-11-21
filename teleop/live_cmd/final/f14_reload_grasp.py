CK_RELOAD = os.path.join(CK_DIR, "0707_act_bc_stage_grasp")
ck_load(CK_RELOAD); gait_on(); op.run(0.3)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync", ex_)
print("RELOADED", CK_RELOAD, "frame", rec.n, state(), flush=True)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\zz_help.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\zz_grasp.py", encoding="utf-8").read())
zz_ip = 136; zz_sd = "right"
print("blanket box", [np.round(v_, 3).tolist() for v_ in garment_box(zz_BL)], "p136", np.round(zz_w().points(0)[zz_ip], 3).tolist(), flush=True)
zz_goal = with_tight(lambda: stance_for(np.r_[zz_w().points(0)[zz_ip][:2], 0.0], zz_sd, X_REL, Y_REL, ignore=(zz_BL,), squat=True, clear_of=(garment_rect(zz_BL),), headings=[np.radians(30.0)]))
print("goal (Fable heading 30)", np.round(zz_goal, 3).tolist(), flush=True)
