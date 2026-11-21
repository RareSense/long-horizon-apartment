exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", "1577_act_hand_over_spot")); gait_on(); sync_cloth(force=True)
b_ = body_of("r107i1_umbrella"); sd_ = "right"
print("loaded", state(), "touch", finger_touch(sd_, b_), flush=True)
mon_start(target=None); MON["held"][sd_] = b_; MON["last_touch"][sd_] = float(d.time)
o_ = {}
try:
    o_["put"] = put_on_floor_oriented(b_, sd_, UMB_SPOT, np.array([0.0, 1.0]), off_tol=0.06, yaw_tol=20.0)
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("PUT", o_, "state", state(), "fell", fallen(), flush=True)
print(close(os.path.join(LK, "u06_entry.jpg"), np.r_[3.6, -1.7, 1.3], np.r_[3.1, -2.45, 0.0], "entry"), look3("u06_put"), flush=True)
