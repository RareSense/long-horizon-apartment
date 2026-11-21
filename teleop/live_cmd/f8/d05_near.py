for b_ in INFO["bodies"]:
    c_ = centre(b_)
    if -5.6 < c_[0] < -4.0 and -1.2 < c_[1] < 1.2:
        lo_, hi_ = obj_box(b_)
        print("thing", INFO["bodies"][b_].get("display", b_), np.round(c_, 2).tolist(), "h", round(float(hi_[2]), 3), flush=True)
