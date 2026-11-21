import numpy as np
for b_,v_ in INFO["bodies"].items():
    try:
        lo_,hi_=obj_box(b_)
    except Exception: continue
    if hi_[0]>-3.3 and lo_[0]<-1.0 and hi_[1]>-2.6 and lo_[1]<-0.9 and lo_[2]<0.5:
        print("OBJ", b_, v_.get("display"), np.round(lo_,2).tolist(), np.round(hi_,2).tolist())
