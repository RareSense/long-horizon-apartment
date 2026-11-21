NSTEP=7
import numpy as np
MON["on"]=False
for k_ in range(NSTEP):
    p_=base()[0]
    if p_[0] > -1.47: break
    kw_=dict(fwd=min(0.12, -1.45 - float(p_[0])), side=float(np.clip(-1.19 - float(p_[1]), -0.04, 0.04)), turn=float(np.clip(-np.degrees(base()[1]), -10, 10)), tag=f"fix1_east{k_}")
    r_=tmove(**kw_); c_=contact_report()
    print("MOVE", {a:round(b,3) if isinstance(b,float) else b for a,b in kw_.items()}, r_["at"], r_["yaw_deg"], r_["fell"], c_["body"], c_["body_who"], r_["look"], flush=True)
    if c_["body"]>3.0 or r_["fell"]: print("STOPPED"); break
