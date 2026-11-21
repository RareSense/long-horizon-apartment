ck_load(os.path.join(RUN, "checkpoints", "0218_act_walk")); gait_on()
exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
TWO["on"] = True; two_keep(4.0); two_keep(1.5)
print("loaded", state()["pelvis"], state()["yaw_deg"], "F", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
def zz_go(wp_, tol_=0.04, final_yaw=None):
    for _k in range(14):
        p_, y_ = base(); v_ = np.asarray(wp_) - p_[:2]; L_ = float(np.linalg.norm(v_))
        if L_ < tol_: break
        dy_ = float(np.degrees(wrapa(np.arctan2(v_[1], v_[0]) - y_)))
        if abs(dy_) > 8.0:
            r_ = tmove(turn=float(np.clip(dy_, -15, 15)), carry=SIDES, tag="pouch_turn")
        else:
            r_ = tmove(fwd=min(0.15, L_), turn=dy_, carry=SIDES, tag="pouch_step")
        print(" mv", r_["at"], r_["yaw_deg"], r_["touch"]["body"], "F", {s_: zz_force(s_) for s_ in SIDES}, flush=True)
    if final_yaw is not None:
        for _k in range(10):
            dy_ = float(np.degrees(wrapa(np.radians(final_yaw) - base()[1])))
            if abs(dy_) < 3.0: break
            r_ = tmove(turn=float(np.clip(dy_, -15, 15)), carry=SIDES, tag="pouch_turn")
            print(" turn", r_["at"], r_["yaw_deg"], r_["touch"]["body"], flush=True)
zz_out = {}
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = (pb_,); MON["ignore"] = {m.body(pb_).id}; MON["t_max"] = 900.0
try:
    zz_go((-4.52, -1.90)); zz_go((-4.52, -1.32)); zz_go((-4.85, -1.05), final_yaw=-125.0)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "F", {s_: zz_force(s_) for s_ in SIDES}, "state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print(look3("pouch_at_basket3"), flush=True)
