ck_load(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\0237_act_transit_east_ok")
mon_start()
for zz_k in range(3):
    p0_, y0_ = base()
    r_ = tmove(fwd=0.12, tag="drift_probe")
    p1_, y1_ = base(); R_ = RM.rz(y0_)[:2, :2].T @ (p1_[:2] - p0_[:2])
    print("step", zz_k, "fwd/left m", np.round(R_, 3).tolist(), "dyaw deg", round(float(np.degrees(wrapa(y1_ - y0_))), 1), "why", MON.get("why"), flush=True)
for zz_k in range(2):
    p0_, y0_ = base()
    r_ = tmove(turn=15.0, tag="drift_probe_t")
    p1_, y1_ = base()
    print("turn", zz_k, "moved m", np.round(p1_[:2] - p0_[:2], 3).tolist(), "dyaw deg", round(float(np.degrees(wrapa(y1_ - y0_))), 1), flush=True)
MON["on"] = False
print("TUCK", TUCK_JOINTS, "TELE", TELE_V, TELE_W, "V_WALK", V_WALK)
