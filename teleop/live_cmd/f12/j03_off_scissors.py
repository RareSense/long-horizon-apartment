MON["on"] = False
sc_ = body_of("r108i1_scissors"); s0_ = centre(sc_).copy()
op.run(2.0, until=_standing); op.run(0.3)
print("contacts", contact_report(), flush=True)
r_ = tmove(side=-0.12, tag="off_scissors")
print("after", state(), "touch", contact_report(), "scissors moved", np.round(centre(sc_) - s0_, 3).tolist(), "fell", fallen(), flush=True)
