pb_ = body_of("r179i1_toy_pouch")
print("ck", ck_save("n1_pouch_held", kind="act", info=dict(note="toy pouch two-hand contact-verified hold on the sill (AI-operated)")), flush=True)
TWO["on"] = True; two_keep(1.0)
def zz_go(wp_, tol_=0.04, final_yaw=None):
    for _k in range(16):
        p_, y_ = base(); v_ = np.asarray(wp_) - p_[:2]; L_ = float(np.linalg.norm(v_))
        if L_ < tol_: break
        dy_ = float(np.degrees(wrapa(np.arctan2(v_[1], v_[0]) - y_)))
        if abs(dy_) > 8.0:
            r_ = tmove(turn=float(np.clip(dy_, -15, 15)), carry=SIDES, tag="pouch_turn")
        else:
            r_ = tmove(fwd=min(0.15, L_), turn=dy_, carry=SIDES, tag="pouch_step")
        print(" mv", r_["at"], r_["yaw_deg"], r_["touch"]["body"], "F", {s_: zz_force(s_, pb_) for s_ in SIDES}, flush=True)
    if final_yaw is not None:
        for _k in range(12):
            dy_ = float(np.degrees(wrapa(np.radians(final_yaw) - base()[1])))
            if abs(dy_) < 3.0: break
            r_ = tmove(turn=float(np.clip(dy_, -15, 15)), carry=SIDES, tag="pouch_turn")
zz_out = {}
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = (pb_,); MON["ignore"] = {m.body(pb_).id}; MON["t_max"] = 1200.0
try:
    for k_ in range(2):
        tmove(fwd=-0.10, carry=SIDES, tag="pouch_back")
    zz_go((-5.30, -2.14)); zz_go((-4.70, -2.00)); zz_go((-4.80, -1.15)); zz_go((-4.85, -1.05), final_yaw=-125.0)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", zz_out, "pouch", np.round(centre(pb_), 3).tolist(), "F", {s_: zz_force(s_, pb_) for s_ in SIDES}, "others", zz_others(pb_), "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
print(look3("n1_pouch_at_basket"), flush=True)
