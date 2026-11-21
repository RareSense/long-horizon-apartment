exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", "0770_act_walk_path")); gait_on(); sync_cloth(force=True)
b_ = body_of("r105i1_shoe"); sd_ = "left"
print("loaded", state(), "touch", finger_touch(sd_, b_), "holding", HOLD.holding(sd_), flush=True)
mon_start(target=None); MON["held"][sd_] = b_; MON["last_touch"][sd_] = float(d.time)
o_ = {}
try:
    st_ = shoe_put_stance(b_, sd_, (1.875, -2.00)); o_["stance"] = np.round(st_, 3).tolist(); print("stance", o_["stance"], flush=True)
    o_["carry"] = walk_tight(st_, carry=(sd_,)).get("err_xy")
    o_["put"] = put_on_floor_oriented(b_, sd_, (1.875, -2.00), np.array([0.0, 1.0]))
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("PUT", o_, "state", state(), "fell", fallen(), flush=True)
print(close(os.path.join(LK, "s03_mat.jpg"), np.r_[1.76, -1.70, 1.3], np.r_[1.76, -2.05, 0.0], "mat"), flush=True)
print(look3("s03_put1"), flush=True)
