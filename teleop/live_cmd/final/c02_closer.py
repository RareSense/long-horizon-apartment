MON["on"] = False
SDp = "right"; pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin")
PRE_ACTION("stand_holding", {}); squat_follow((SDp,), 0.0, 0.0)
print("stood", state(), "held", HOLD.holding(SDp), flush=True)
r_ = tmove(fwd=0.07, carry=(SDp,), tag="closer_bin")
print("after", state(), "touch", contact_report(), "held", HOLD.holding(SDp), "paper", np.round(centre(pb_), 3).tolist(), "fell", fallen(), flush=True)
print("look", r_.get("look") if isinstance(r_, dict) else r_, flush=True)
