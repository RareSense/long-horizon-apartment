# AI-operated (Fable escalation, scooter r126): tilt 4.4 deg, rear wheel 0.405 of 0.44, the bar at the left pads' edge
# (seat -14.1). The ending found in Chain 22: both squeezes eased to 6 N (and the told load taken off) so the bar leaves the
# jaws and the scooter comes down the last centimetres onto its front wheels. Watched every 0.2 s.
print("ck", ck_save("fsc_before_ease", kind="act", info=dict(note="scooter tilt 4.4 deg on its rear wheel, bar in both jaws, before easing the squeeze (AI-operated)")), flush=True)
mon_start(target=sc_); MON["t_max"] = 6000.0
MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
try:
    for s_ in SIDES:
        ts.ctrl.ext.pop(f"hold_{s_}", None)
        jaw_force[s_] = 6.0
    for k_ in range(12):
        op.run(0.2)
        st_ = sh_state(sc_)
        print(f"[ease {k_}] t {d.time:.2f} tilt {st_['tilt']} bar {st_['bar']} floor {sh_on_floor(sc_)} touch {st_['touch']} gap {st_['gap']} pads z", {s_: round(float(pad_mid(s_)[2]), 3) for s_ in SIDES}, "why", MON.get("why"), flush=True)
        if len(sh_on_floor(sc_)) >= 2 and st_["tilt"] < 2.0 and k_ >= 4:
            break
    MON["held"] = {}; MON["target"] = sc_
    sd_rep("eased")
    lo_, hi_ = obj_box(sc_)
    print("box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "centre", np.round(centre(sc_), 3).tolist(), "fallen", fallen(), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
MON["on"] = False
views("e05")
