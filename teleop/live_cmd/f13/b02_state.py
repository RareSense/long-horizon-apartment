MON["on"] = False
pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin")
print("paper", np.round(centre(pb_), 3).tolist(), "in bin", inside(pb_, bn_), "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "state", state(), "fell", fallen(), "touch", contact_report()["body"], flush=True)
print("last events", EVENTS[-4:], flush=True)
