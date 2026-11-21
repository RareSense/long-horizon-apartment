# AI-operated (Fable escalation, scooter r126): reload "stance back" (hands at rest), raise both open hands 9 cm behind the
# bar (the reach that worked in b00), then step IN 7 cm with the hands riding (b01: with the arms out the pelvis leans 6 cm
# back and the cross-body left pad came 2.9 cm short of its place on the bar). Look.
print("REC before reload", rec.n, flush=True)
ck_load(os.path.join(RUN, "checkpoints", "3862_act_fsc_stance_back")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.5); rec.still_every = 300
print("RELOADED 3862 rec", rec.n, state(), flush=True)
exec(open(r"E:\urc_final\scripts\home\live\scooter_hang.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
CK_STATE["item"] = f"{POS + 1:03d}_{nm}"
FSC_OLD = (TELE_V, TELE_W, globals().get("CARRY_LOW"))
TELE_V = V_CARRY_HEAVY; TELE_W = 0.10; CARRY_LOW = False
mon_start(target=sc_); MON["t_max"] = 6000.0
try:
    op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.6)); op.run(0.9)
    for s_ in SIDES:
        jaw_force[s_] = 20.0; jaw_target[s_] = JAW_OPEN
        ts.setup.end_effectors[s_]["rot_weight"] = float(SH["rot_weight"])
    tg_, Q_, F_ = sh_targets(sc_, back=0.09)
    e1_ = both_move(tg_, Q_, speed=0.15, tol=0.006)
    print("pre_err", e1_, flush=True)
    diag("pre", tg_)
    r_ = tmove(fwd=0.07, carry=tuple(SIDES), tag="fsc_step_in")
    print("step in", r_["at"], r_["yaw_deg"], r_["touch"], "why", MON.get("why"), flush=True)
    tg_, Q_, F_ = sh_targets(sc_, back=0.09)
    diag("stepped", tg_)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
views("c00")
print("mem", mem(), flush=True)
