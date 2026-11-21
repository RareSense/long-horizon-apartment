# AI-operated (Fable escalation, scooter r126): the wheel plant did not take the weight off the pads (lower pads still 15 N,
# the right fingers pitched 19 deg): that branch is dropped. Reload "before plant" (scooter hanging, facing south).
# Probe 1: the left hand alone 1.5 cm straight back (toward the robot): does the bar roll back toward the pads' middle?
print("REC before reload", rec.n, flush=True)
ck_load(os.path.join(RUN, "checkpoints", "3966_act_fsc_before_plant")); gait_on(); settle_after_load(); refresh_jointed_footprints(); op.run(1.0); rec.still_every = 300
print("RELOADED 3966 rec", rec.n, state(), flush=True)
exec(open(r"E:\urc_final\scripts\home\live\scooter_hang.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fable_sc\lib.py", encoding="utf-8").read())
sh_recentre.__defaults__ = (0.35, 0.025, 0.03)
CK_STATE["item"] = f"{POS + 1:03d}_{nm}"
TELE_V = V_CARRY_HEAVY; TELE_W = 0.10; CARRY_LOW = False
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
print("jaw actuator ranges", {s_: (m.actuator_ctrlrange[jaw_a[s_]].tolist(), m.actuator_forcerange[jaw_a[s_]].tolist(), float(m.actuator_gear[jaw_a[s_]][0])) for s_ in SIDES}, "jaw_force", jaw_force, "rot_weight", {s_: ts.setup.end_effectors[s_].get("rot_weight") for s_ in SIDES}, "ext", list(ts.ctrl.ext.keys()), flush=True)


def rep(tag):
    st_ = sh_state(sc_)
    print(f"[{tag}] bar", st_["bar"], "bar_rel", st_["bar_rel"], "deck-yaw", round(st_["deck_deg"] - 180 - st_["yaw"], 1), "tilt", st_["tilt"], "along", st_["along"], "pad_to_bar", st_["pad_to_bar"], "touch", st_["touch"], "seat", sh_seat(sc_),
          "floor", sh_on_floor(sc_), "why", MON.get("why"), "rec", rec.n, flush=True)


try:
    rep("loaded")
    p_, y_ = base(); f3_ = np.array([np.cos(y_), np.sin(y_), 0.0])
    seat_ = sh_seat(sc_)
    PRE_ACTION("fsc_probe_left_back", dict(d=0.015))
    both_move({"left": pad_mid("left") - f3_ * 0.015, "right": pad_mid("right").copy()}, sh_level_Q({s_: seat_[s_]["pitch"] for s_ in SIDES}), speed=0.02, tol=0.004)
    op.run(0.5)
    rep("left back 1.5 cm")
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
views("d00")
