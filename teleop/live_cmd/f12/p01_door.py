MON["on"] = False
op.run(1.0)
print("state", state(), "fell", fallen(), flush=True)
exec(open(r"E:\urc_fable3\scripts\home\kitchen_skills.py", encoding="utf-8").read())
A_, ax_, a_, bid_, j_ = hinge_axis("r159i1_door")
print("door q", round(float(d.qpos[a_]), 3), "range", np.round(m.jnt_range[j_], 3).tolist(), "vehicle", np.round(centre(body_of("r191i1_toy_vehicle")), 2).tolist(), flush=True)
floor_first(["r159i1_door"])
zz_d = call_mon(lambda: close_door_follow("r159i1_door"), "r159i1_door", target=m.body(bid_).name, ck=False)
print("DOOR", {k_: v_ for k_, v_ in zz_d.items() if k_ in ("status", "why", "sim_s", "wall_s", "look")}, "rec", str(zz_d.get("record"))[:600], flush=True)
print("door q now", round(float(d.qpos[a_]), 3), "state", state(), "fell", fallen(), flush=True)
if zz_d.get("status") == "done":
    print("DONE", item_done_auto("r159i1_door", dict(status="done", how="kitchen_skills.close_door_follow under call_mon (the toy vehicle r191 no longer by the door) (AI-operated)")), flush=True)
