MON["on"] = False; HELD.pop("left", None); op.run(1.0)
lo_, hi_ = obj_box(zz_bin); c_ = centre(zz_b)
print("bag", np.round(c_, 3).tolist(), "in bin", bool(lo_[0] < c_[0] < hi_[0] and lo_[1] < c_[1] < hi_[1] and c_[2] < hi_[2]), "inside()", inside(zz_b, zz_bin), "bin", [np.round(v_, 3).tolist() for v_ in obj_box(zz_bin)], "state", state(), "touch", contact_report(), "jaw", jaw("left"), flush=True)
print(look3("bag_in_bin"), flush=True)
