MON["on"] = False
bn_ = body_of("rubbish_bin")
print("before", state(), "bin", np.round(centre(bn_), 3).tolist(), "touch", contact_report(), flush=True)
r_ = tmove(fwd=-0.08, side=-0.06, carry=("left",), tag="off_bin")
print("after", state(), "touch", contact_report(), "held", HOLD.holding("left"), "fell", fallen(), flush=True)
print("look", r_.get("look") if isinstance(r_, dict) else r_, flush=True)
