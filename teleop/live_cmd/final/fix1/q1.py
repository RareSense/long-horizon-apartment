import numpy as np
print("STATE", state(), "POS", POS, "rec", rec.n, "fallen", fallen())
c_=contact_report(); print("CONTACT", c_["body"], c_["body_who"])
for n_ in ("r133i1_laundry_basket","r126i1_scooter","r186i1_basket","r68i1_rag","rubbish_bin"):
    try:
        b_=body_of(n_) or n_; bx_=obj_box(b_); print("BOX", n_, b_, np.round(bx_[0],3).tolist(), np.round(bx_[1],3).tolist())
    except Exception as ex_: print("ERR", n_, ex_)
print("BASE", np.round(base()[0],3).tolist(), round(float(np.degrees(base()[1])),1))
