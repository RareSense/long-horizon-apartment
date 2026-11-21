zz_bin = body_of("rubbish_bin")
print("bin box", [np.round(v_, 3).tolist() for v_ in obj_box(zz_bin)], "touch", contact_report(), "state", state(), flush=True)
print("near", near_things(0.9), flush=True)
