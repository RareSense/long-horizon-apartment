# AI teleop fix for the r193i3 set-aside (AI-operated): back to the checkpoint before the set-down (crouched, toy held in
# the right jaws), a spot with room (the pocket's north end, 0.15 m east of r193i1), set down there under the monitor.
ck_load(os.path.join(RUN, "checkpoints", "0203_act_crouch_holding"))
gait_on(); op.run(0.5)
zz_b = body_of("r193i3_toy_piece"); zz_disp = INFO["bodies"][zz_b].get("display", "r193i3_toy_piece")
print("at 0203", state(), "toy", np.round(centre(zz_b), 3).tolist(), "HELD", list(HELD), "bottle", np.round(centre(body_of("r155i1_kids_bottle")), 3).tolist(), flush=True)
print("look", look3("aside_fix_0203"), flush=True)
zz_old = (DESC["destinations"].get(zz_disp), DESC["spots"].get(zz_disp))
DESC["destinations"][zz_disp] = "floor"; DESC["spots"][zz_disp] = [ZZ_SPOT[0], ZZ_SPOT[1]]
mon_start(target=None); MON["ignore_names"] = (body_of("r192i1_ball"),)
MON["held"]["right"] = zz_b; MON["last_touch"]["right"] = float(d.time)
try:
    zz_puts = put_away_any(zz_b, "right")
    zz_pt = zz_puts[-1] if zz_puts else {}
    print("PUT", {k: (v if not isinstance(v, (dict, list)) else str(v)[:200]) for k, v in zz_pt.items() if k != "walk"}, flush=True)
except Exception as ex:
    import traceback as _tb
    print("PUT ERR", _tb.format_exc()[-600:], flush=True)
MON["on"] = False; MON["held"].pop("right", None)
DESC["destinations"][zz_disp], DESC["spots"][zz_disp] = zz_old
print("END", MON.get("why"), state(), "toy", np.round(centre(zz_b), 3).tolist(), "bottle", np.round(centre(body_of("r155i1_kids_bottle")), 3).tolist(), "touch", contact_report(), look3("aside_fix_end"), flush=True)
