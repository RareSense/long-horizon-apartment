import numpy as np, json
MON["on"]=False
for kw_ in json.loads(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\fix1\mv.json").read()):
    r_=tmove(**kw_)
    c_=contact_report(); print("MOVE", kw_, r_["at"], r_["yaw_deg"], r_["fell"], c_["body"], c_["body_who"], r_["look"], flush=True)
    if c_["body"]>3.0 or r_["fell"]: print("STOPPED"); break
