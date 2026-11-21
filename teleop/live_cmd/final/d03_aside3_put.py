# r193i3 aside, AI teleop fix (AI-operated): from 0342 (toy held left, ball r192 0.2 m ahead) step BACK away from the
# ball first, then the library put-down at the aside spot under the monitor.
zz_b = body_of("r193i3_toy_piece"); zz_disp = INFO["bodies"][zz_b].get("display", "r193i3_toy_piece")
r_ = tmove(fwd=-0.12, carry=("left",), tag="aside3_back")
print("BACK", state(), "touch", contact_report(), "ball", np.round(centre(body_of("r192i1_ball")), 3).tolist(), flush=True)
zz_old = (DESC["destinations"].get(zz_disp), DESC["spots"].get(zz_disp))
DESC["destinations"][zz_disp] = "floor"; DESC["spots"][zz_disp] = [-2.79, -0.605]
mon_start(target=None)
MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
zz_pt = {}
try:
    zz_puts = put_away_any(zz_b, "left")
    zz_pt = zz_puts[-1] if zz_puts else {}
    print("PUT", {k: (v if not isinstance(v, (dict, list)) else str(v)[:200]) for k, v in zz_pt.items() if k != "walk"}, flush=True)
except Exception as ex:
    import traceback as _tb
    print("PUT ERR", _tb.format_exc()[-600:], flush=True)
why_ = MON.get("why")
MON["on"] = False; MON["held"].pop("left", None)
DESC["destinations"][zz_disp], DESC["spots"][zz_disp] = zz_old
print("END", why_, state(), "toy", np.round(centre(zz_b), 3).tolist(), "ball", np.round(centre(body_of("r192i1_ball")), 3).tolist(), "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "fell", fallen(), "touch", contact_report(), flush=True)
print(look3("aside3_end"), flush=True)
if zz_pt.get("ok") and not why_ and not fallen() and not any(HOLD.holding(s_) for s_ in SIDES):
    ASIDE.append((zz_disp, [-2.79, -0.605], zz_old[0])); RESULT["aside"] = list(ASIDE)
    print("CK", ck_save("aside_r193i3_toy_piece", kind="item", info=dict(aside=True, note="set aside (not a route item); teleop step back from the ball first, AI-operated")), flush=True)
