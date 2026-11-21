exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
MON["on"] = False
zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", "0768_act_carry_pose")); gait_on(); sync_cloth(force=True)
b_ = body_of("r105i1_shoe"); sd_ = "left"
ax_, c_, zb_ = shoe_axis(b_)
print("at 0768", state(), "touch", finger_touch(sd_, b_), "axis", np.round(ax_, 2).tolist(), "c", np.round(c_, 3).tolist(), "zb", round(zb_, 3), "tilt", round(box_tilt_deg(b_), 1), "pad", np.round(pad_mid(sd_), 3).tolist(), flush=True)
print(look_hand(sd_, "s05_held_0768"), flush=True)
mon_start(target=None); MON["held"][sd_] = b_; MON["last_touch"][sd_] = float(d.time)
o_ = {}
try:
    st_ = shoe_put_stance(b_, sd_, (1.875, -2.00)); o_["stance"] = np.round(st_, 3).tolist(); print("stance", o_["stance"], flush=True)
    o_["carry"] = walk_tight(st_, carry=(sd_,)).get("err_xy")
    ax_, c_, zb_ = shoe_axis(b_)
    print("arrived", state(), "touch", finger_touch(sd_, b_), "axis", np.round(ax_, 2).tolist(), "c", np.round(c_, 3).tolist(), "zb", round(zb_, 3), "tilt", round(box_tilt_deg(b_), 1), flush=True)
    print(look_hand(sd_, "s05_arrived"), flush=True)
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
print("CARRY", o_, "fell", fallen(), flush=True)
