import ast

p = r"E:\urc_gait\src\urc\locomotion\biped.py"
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


rep("""_PLAN = dict(plan=False, plan_dmax=[0.02, 0.012], plan_k=12.0, plan_tol=0.006, plan_ds_max=0.45, plan_stop_tol=0.012, plan_extra=6,
             plan_emax=0.15, plan_width=0.85, plan_gain=1.0, plan_rate=1.0)
""", """_PLAN = dict(plan=False, plan_dmax=[0.015, 0.012], plan_k=12.0, plan_tol=0.006, plan_ds_max=0.45, plan_stop_tol=0.008, plan_extra=6,
             plan_emax=0.15, plan_lead=0.04, plan_width=0.85, plan_gain=1.0, plan_rate=1.0)
""")
rep("""    def _plan_measure(self, soles):
        \"\"\"Both feet down: the soles' middle against the plan. An anchor further than plan_emax from where the robot
        stands is pulled along (a blocked robot does not wind up).\"\"\"
        g = self.g
        mid, _ = self._plan_mid(0.0, np.zeros(3))
        e = 0.5 * (soles[0][:2] + soles[1][:2]) - mid
        n = float(np.linalg.norm(e))
""", """    def _plan_measure(self, soles):
        \"\"\"Both feet down: the soles' middle against the plan. An anchor further than plan_emax from where the robot
        stands is pulled along (a blocked robot does not wind up). And along the way it is asked to go, the anchor
        never leads the robot by more than plan_lead: starting a leg at 0.18 m/s the anchor was 8-11 cm ahead after
        two steps and the walk caught up with 13 cm steps on a 7 cm gait; carrying, at the normal height with nearly
        straight knees, a 0.5 m backward leg fell that way (Isaac regression leg_carry_back, 20 Nov 2026).\"\"\"
        g = self.g
        mid, _ = self._plan_mid(0.0, np.zeros(3))
        e = 0.5 * (soles[0][:2] + soles[1][:2]) - mid
        vw = _rz(self.yaw_ref)[:2, :2] @ np.asarray(self.v_filt[:2], float)
        nv = float(np.linalg.norm(vw))
        if nv > 0.02:
            lead = -float(e @ vw) / nv
            if lead > g["plan_lead"]:
                self.anc = self.anc - vw / nv * (lead - g["plan_lead"])
                e = e + vw / nv * (lead - g["plan_lead"])
        n = float(np.linalg.norm(e))
""")
ast.parse(s)
open(p, "w", encoding="utf-8").write(s)

p = r"E:\urc_gait\scripts\home\skills.py"
s = open(p, encoding="utf-8").read()
rep("""        if st_["rest"] < 0.003:
            return dict(cmd="base", vx=0.0, vy=0.0, wz=0.0, ttl=3 * op.period)
        return dict(cmd="base", vx=float(sgn * np.clip(0.8 * st_["rest"], 0.05, vmax)), vy=0.0, wz=0.0, ttl=3 * op.period)
""", """        if st_["rest"] < 0.003:
            return dict(cmd="base", vx=0.0, vy=0.0, wz=0.0, ttl=3 * op.period)
        # the anchor is brought onto the line through the goal by a small side speed (planned footholds only): a leg
        # begun 3 cm beside its line ended 2.7 cm beside the goal (Isaac regression leg_off_rug_back, 20 Nov 2026)
        vy_ = float(np.clip(1.0 * float((g_ - ref) @ nl), -0.03, 0.03)) if lo_.g.get("plan") else 0.0
        return dict(cmd="base", vx=float(sgn * np.clip(0.8 * st_["rest"], 0.05, vmax)), vy=vy_, wz=0.0, ttl=3 * op.period)
""")
rep("""    u = sgn * np.array([np.cos(head), np.sin(head)])
    g_ = np.asarray(goal_xy, float)[:2]
    p_start = base()[0][:2].copy()
    st_ = dict(rest=float((g_ - p_start) @ u))
""", """    u = sgn * np.array([np.cos(head), np.sin(head)])
    nl = np.array([-np.sin(head), np.cos(head)])        # to the left of the heading
    g_ = np.asarray(goal_xy, float)[:2]
    p_start = base()[0][:2].copy()
    st_ = dict(rest=float((g_ - p_start) @ u))
""")
rep("""            p, yaw = base()
            if float(np.hypot(gx - p[0], gy - p[1])) > tol:
                _leg_by_anchor_xy((gx, gy), hands, V_CARRY_HEAVY if (carry and _held_kg() >= HEAVY_KG) else V_SHORT)
            if fallen():
                raise RuntimeError("the robot fell while walking")
            p, yaw = base()
            if float(np.hypot(gx - p[0], gy - p[1])) <= tol and abs(wrapa(gyaw - yaw)) < 0.06:
                break
            continue
""", """            p, yaw = base()
            tol_p = min(tol, PLAN_TOL)
            if float(np.hypot(gx - p[0], gy - p[1])) > tol_p:
                _leg_by_anchor_xy((gx, gy), hands, V_CARRY_HEAVY if (carry and _held_kg() >= HEAVY_KG) else V_SHORT)
            if fallen():
                raise RuntimeError("the robot fell while walking")
            p, yaw = base()
            if float(np.hypot(gx - p[0], gy - p[1])) <= max(tol_p, 0.015) and abs(wrapa(gyaw - yaw)) < 0.06:
                break
            continue
""")
rep("""SHORT_NO_TURN, V_SHORT = 0.45, (0.12, 0.06)        # see _leg_by_anchor_xy
""", """SHORT_NO_TURN, V_SHORT = 0.45, (0.12, 0.06)        # see _leg_by_anchor_xy
PLAN_TOL = 0.015                                   # walking on planned footholds: what is left over this is walked as one more short leg
V_ANCHOR_CARRY = 0.12                              # leg speed by the anchor with something light in a hand (0.18: see walk)
""")
rep("""                _leg_by_anchor((gx, gy), -1.0 if back else 1.0, hands, V_CARRY_HEAVY if (carry and _held_kg() >= HEAVY_KG) else V_ANCHOR)
""", """                _leg_by_anchor((gx, gy), -1.0 if back else 1.0, hands, V_CARRY_HEAVY if (carry and _held_kg() >= HEAVY_KG) else (V_ANCHOR_CARRY if carry else V_ANCHOR))
""")
ast.parse(s)
open(p, "w", encoding="utf-8").write(s)
print("patched")
