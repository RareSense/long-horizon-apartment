# AI-operated (Fable escalation, scooter r126): reload 3697, load the skill, look at where things are. No motion.
nm = "r126i1_scooter"; sc_ = body_of(nm)
print("REC before reload", rec.n, flush=True)
ck_load(os.path.join(RUN, "checkpoints", "3697_act_n1_scooter_pre")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.5); rec.still_every = 300
print("RELOADED 3697 rec", rec.n, state(), flush=True)
exec(open(r"E:\urc_final\scripts\home\live\scooter_hang.py", encoding="utf-8").read())
SC_NAME = nm
F_ = sh_frame(sc_)
print("frame c", np.round(F_["c"], 3), "z", round(F_["z"], 3), "f", np.round(F_["f"], 3), "lft", np.round(F_["lft"], 3), "bar_half", round(F_["sp"]["bar_half"], 3), "thick", round(F_["sp"]["bar_thick"], 3), "depth", round(F_["sp"]["bar_depth"], 3), flush=True)
print("stance", np.round(sh_stance(sc_), 3), "box", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], flush=True)
print("wheel", {k_: (round(v_, 3) if isinstance(v_, float) else v_) for k_, v_ in sh_wheel(sc_).items() if k_ != "arc"}, flush=True)
print("TELE_V", TELE_V, "V_CARRY_HEAVY", V_CARRY_HEAVY, "plan", ts.loco.g.get("plan"), "hold", ts.loco.g.get("hold"), "CK n", CK_STATE["n"], "POS", POS, flush=True)
print("mass", float(m.body_subtreemass[m.body(nm).id]) if hasattr(m, "body_subtreemass") else None, flush=True)
print("LOOK", look3("fsc_a00"), flush=True)
