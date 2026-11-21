MON["on"] = False
ck_load(os.path.join(RUN, "checkpoints", "0182_item_r125i1_flat")); gait_on(); settle_after_load(); refresh_jointed_footprints()
print(floor_first(["r120i1_duck"])[:2], flush=True)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f9\zz_pick_here.py", encoding="utf-8").read())
mon_start(target=zz_b)
try:
    r_ = tmove(fwd=-0.12, tag="off_lamp"); print("back", r_["at"], r_["yaw_deg"], r_["touch"], flush=True)
    for k_ in range(12):
        e_ = float(np.degrees(wrapa(np.pi / 2 - base()[1])))
        if abs(e_) < 3: break
        r_ = tmove(turn=float(np.clip(abs(e_), 0, 15)), tag="turn_north"); print("turn", r_["at"], r_["yaw_deg"], r_["touch"]["body"], flush=True)
    print("reach", in_reach(grasp_plan(zz_b)["point"], "right"), "duck", np.round(centre(zz_b), 3).tolist(), flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("state", state(), flush=True); print(look3("faced_north"), flush=True)
