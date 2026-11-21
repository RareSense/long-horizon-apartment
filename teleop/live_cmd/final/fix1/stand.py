MON["on"]=False
print("BEFORE", state(), fallen(), flush=True)
PRE_ACTION("crouch", dict(h=0.0, l=0.0)); crouch(0.0, 0.0, T=1.6)
rest_hands(SIDES); op.run(1.0)
c_=contact_report()
print("AFTER", state(), fallen(), c_["body"], c_["body_who"], look3("fix1_stand"), flush=True)
