MON["on"] = False
b0_ = centre(binb_).copy()
r_ = tmove(fwd=-0.10, tag="off_bin2")
print("after", state(), "touch", contact_report()["body"], "bin moved", round(float(np.linalg.norm(centre(binb_) - b0_)), 4), "pouch in", inside(zz_b, binb_), flush=True)
r_ = tmove(fwd=-0.10, tag="off_bin3")
print("after", state(), "touch", contact_report()["body"], "fell", fallen(), flush=True)
