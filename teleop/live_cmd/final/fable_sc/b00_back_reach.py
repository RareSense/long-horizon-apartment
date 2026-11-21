# AI-operated (Fable escalation, scooter r126): reload the at-stance checkpoint, step back 12 cm (bar 0.38 ahead: room for
# the right forearm to point forward with the elbow down), hands 9 cm behind the bar in free air. Look.
print("REC before reload", rec.n, flush=True)
ck_load(os.path.join(RUN, "checkpoints", "3854_act_fsc_at_stance")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.5); rec.still_every = 300
print("RELOADED 3854 rec", rec.n, state(), flush=True)
exec(open(r"E:\urc_final\scripts\home\live\scooter_hang.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
CK_STATE["item"] = f"{POS + 1:03d}_{nm}"
mon_start(target=sc_); MON["t_max"] = 6000.0
try:
    r_ = tmove(fwd=-0.12, tag="fsc_back")
    print("back", r_["at"], r_["yaw_deg"], r_["touch"], "why", MON.get("why"), flush=True)
    diag("back")
    print("ck", ck_save("fsc_stance_back", kind="act", info=dict(note="scooter take stance 12 cm further back, hands empty (AI-operated)")), flush=True)
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.9)
    for s_ in SIDES:
        jaw_force[s_] = 20.0; jaw_target[s_] = JAW_OPEN
        ts.setup.end_effectors[s_]["rot_weight"] = float(SH["rot_weight"])
    tg_, Q_, F_ = sh_targets(sc_, back=0.09)
    e1_ = both_move(tg_, Q_, speed=0.15, tol=0.006)
    print("pre_err", e1_, flush=True)
    diag("pre", tg_)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
views("b00")
