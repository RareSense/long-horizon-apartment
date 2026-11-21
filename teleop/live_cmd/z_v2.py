ck_load(ZZ_CK); print(gait_on()); mon_start()
p0_, y0_ = base(); zz_tr = []
for _k in range(6):
    r_ = tmove(turn=15.0, tag="v_turn")
    zz_tr.append((r_["at"], r_["yaw_deg"]))
    if MON.get("why"):
        break
p1_, y1_ = base()
print("tmove turn90", dict(moved_m=round(float(np.linalg.norm(p1_[:2] - p0_[:2])), 3), dyaw=round(float(np.degrees(wrapa(y1_ - y0_))), 1), why=MON.get("why")), zz_tr, flush=True)
print("W_TURN", W_TURN, "W_TURN_CARRY", W_TURN_CARRY)
ck_load(ZZ_CK); gait_on(); mon_start(); MON["trace"] = []
p0_, y0_ = base()
try:
    _turn_on_spot(float(y0_ + np.pi / 2), hand_cmds(()), tol=0.05); _settle_stop(hand_cmds(()))
except Exception as ex:
    print("ex", str(ex)[:200])
p1_, y1_ = base()
print("spot turn90", dict(moved_m=round(float(np.linalg.norm(p1_[:2] - p0_[:2])), 3), dyaw=round(float(np.degrees(wrapa(y1_ - y0_))), 1), why=MON.get("why")), "trace", MON["trace"][::3], flush=True)
MON["trace"] = None; MON["on"] = False
