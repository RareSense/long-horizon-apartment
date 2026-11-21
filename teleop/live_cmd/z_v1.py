hot_reload(r"E:\urc_home\scripts\home\gait\gait_test.py", ["gt_reload_gait"])
exec(open(r"E:\urc_home\scripts\home\live\ops.py", encoding="utf-8").read())


def gait_on():
    """home-gait eb5a8a3 (merged 8001a76): the gait's position hold ON, arms at rest (coordinator 19 Nov ~23:55)."""
    global TUCK_JOINTS
    TUCK_JOINTS = False
    return gt_reload_gait(hold=True)


ZZ_CK = r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok"
zz_res = {}
# (a) a 90 deg turn on the spot (walk to the same place, yaw + 90)
ck_load(ZZ_CK); print(gait_on()); mon_start()
p0_, y0_ = base()
try:
    walk((float(p0_[0]), float(p0_[1]), float(y0_ + np.pi / 2)))
except Exception as ex:
    print("turn ex", str(ex)[:200])
p1_, y1_ = base()
zz_res["turn90"] = dict(moved_m=round(float(np.linalg.norm(p1_[:2] - p0_[:2])), 3), dyaw=round(float(np.degrees(wrapa(y1_ - y0_))), 1), why=MON.get("why"))
print("turn90", zz_res["turn90"], flush=True)
# (b) a 0.4 m leg (diagonal north-east, along the heading 30 deg it stands at)
ck_load(ZZ_CK); gait_on(); mon_start()
p0_, y0_ = base(); zz_g = p0_[:2] + 0.4 * np.array([np.cos(y0_), np.sin(y0_)])
try:
    walk((float(zz_g[0]), float(zz_g[1]), float(y0_)))
except Exception as ex:
    print("leg ex", str(ex)[:200])
p1_, y1_ = base()
zz_res["leg04"] = dict(goal=np.round(zz_g, 3).tolist(), at=np.round(p1_[:2], 3).tolist(), err_m=round(float(np.linalg.norm(p1_[:2] - zz_g)), 3), why=MON.get("why"))
print("leg04", zz_res["leg04"], flush=True)
# (c) short re-aimed steps toward (-0.85,-0.85)
ck_load(ZZ_CK); gait_on()
zz_ok, zz_log = step_to([(-0.85, -0.85)], tols=[0.08])
zz_res["steps"] = dict(ok=zz_ok, n=len(zz_log), end=zz_log[-1] if zz_log else None, err_m=round(aim((-0.85, -0.85))[1], 3))
print("steps", zz_res["steps"], flush=True)
print("RESULT", zz_res, kit_mem())
