MON["on"] = False
op.send(dict(cmd="base", vx=0.0, vy=0.0, wz=0.0)); op.run(3.0, until=_standing); op.run(0.5)
tw_ = body_of("r100i1_towel"); p0_ = centre(tw_).copy()
print("state", state(), "fell", fallen(), "towel", np.round(p0_, 3).tolist(), "dist", round(float(np.linalg.norm(p0_[:2] - base()[0][:2])), 3), flush=True)
print("towel contacts", umb_contacts(tw_)[:8], flush=True)
op.run(3.0)
print("towel after 3 s standing", np.round(centre(tw_), 3).tolist(), "moved", round(float(np.linalg.norm(centre(tw_) - p0_)), 4), flush=True)
