import numpy as np
MON["on"]=False
r_=tmove(side=0.08, tag="fix1_m1")
c_=contact_report(); print("MOVE", r_["at"], r_["yaw_deg"], r_["fell"], c_["body"], c_["body_who"], r_["look"])
