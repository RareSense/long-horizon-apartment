# TV-cabinet door r159 shut (AI-operated): kitchen_skills.close_door_follow under call_mon from the chain end.
# close_door_follow does ceil(remaining/20 deg)+2 stages; the last try made ~10.5 deg a stage, so it is called again
# (same call, from where the door is) while each call makes progress, at most 3 calls.
MON["on"] = False
op.run(1.0)
print("state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
exec(open(r"E:\urc_fable3\scripts\home\kitchen_skills.py", encoding="utf-8").read())
A_, ax_, a_, bid_, j_ = hinge_axis("r159i1_door")
print("door q", round(float(d.qpos[a_]), 3), "range", np.round(m.jnt_range[j_], 3).tolist(), "vehicle", np.round(centre(body_of("r191i1_toy_vehicle")), 2).tolist(), flush=True)
floor_first(["r159i1_door"])
print("route head", item_name(ROUTE[POS]), flush=True)


def door_all():
    recs = []
    for i_ in range(3):
        q0_ = float(d.qpos[a_])
        r_ = close_door_follow("r159i1_door")
        recs.append({k_: r_.get(k_) for k_ in ("q0", "q", "shut", "ok", "error", "stages")})
        print("[door_all] call", i_, "q", round(q0_, 3), "->", r_.get("q"), "ok", r_.get("ok"), "kit", kit_mem(), flush=True)
        if r_.get("ok") or robot_down() or abs(float(d.qpos[a_]) - q0_) < np.radians(2.0):
            break
        PRE_ACTION("door_follow_again", dict(q=round(float(d.qpos[a_]), 3)))
    return dict(ok=bool(recs and recs[-1].get("ok")), calls=recs, error=None if (recs and recs[-1].get("ok")) else "not shut")


zz_d = call_mon(door_all, "r159i1_door", target=m.body(bid_).name, ck=False, t_max=3600.0)
print("DOOR", {k_: v_ for k_, v_ in zz_d.items() if k_ in ("status", "why", "sim_s", "wall_s", "look")}, "rec", str(zz_d.get("record"))[:900], flush=True)
print("door q now", round(float(d.qpos[a_]), 3), "state", state(), "fell", fallen(), "kit", kit_mem(), flush=True)
