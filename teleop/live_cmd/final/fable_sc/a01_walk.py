# AI-operated (Fable escalation, scooter r126): stage 1 = the skill's own walk to the take stance, then stop and look.
nm = "r126i1_scooter"; sc_ = body_of(nm); SC_NAME = nm
CK_STATE["item"] = f"{POS + 1:03d}_{nm}"
mon_start(target=sc_); MON["t_max"] = 6000.0
try:
    st_ = sh_stance(sc_); f_ = np.array([np.cos(st_[2]), np.sin(st_[2])])
    pre_ = (float(st_[0] - SH_PARK["pre_back"] * f_[0]), float(st_[1] - SH_PARK["pre_back"] * f_[1]), st_[2])
    print("stance", np.round(st_, 3), "pre", np.round(pre_, 3), flush=True)
    walk_via(list(SH_PARK["approach"]) + [(SH_PARK["approach"][-1][0], pre_[1] + 0.02), pre_])
    print("at pre", state()["pelvis"], state()["yaw_deg"], "why", MON.get("why"), flush=True)
    if not MON.get("why"):
        walk(st_)
    print("after walk", state(), "why", MON.get("why"), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
p_, y_ = base(); F_ = sh_frame(sc_)
rel_ = RM.rz(y_)[:2, :2].T @ (F_["c"] - p_[:2])
print("pelvis", np.round(p_, 3), "yaw", round(float(np.degrees(y_)), 1), "bar_rel (ahead, left)", np.round(rel_, 3), "want", [SH["D"], -SH["off"]], "box", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], "fallen", fallen(), flush=True)
print("touch", contact_report() if "contact_report" in globals() else None, flush=True)
print("rec", rec.n, "LOOK", look3("fsc_a01_stance"), flush=True)
