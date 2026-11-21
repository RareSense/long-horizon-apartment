MON["on"] = False
op.send(dict(cmd="base", vx=0.0, vy=0.0, wz=0.0))
op.run(3.0, until=_standing); op.run(1.0)
print("state", state(), "fell", fallen(), "touch", contact_report(), flush=True)
print(look3("f12_wrap_settle"), flush=True)
