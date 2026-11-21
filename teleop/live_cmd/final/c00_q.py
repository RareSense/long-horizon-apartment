pb_ = body_of("r195i1_paper"); bn_ = body_of("rubbish_bin")
print("paper", np.round(centre(pb_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(pb_)], "dest", DESC["destinations"].get("r195i1_paper"), flush=True)
print("bin", np.round(centre(bn_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(bn_)], "state", state(), flush=True)
