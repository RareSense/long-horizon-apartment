zz_n = "r116i1_coat_pile"
zz_r = bigcloth_into(zz_n, s1="right", start="free1", stop_after="free1")
print("RESULT", zz_r, flush=True)
print("inside", in_container(zz_n, laundry_body()), "out", bc_out(zz_n, laundry_body()), "fold target", bc_fold_target(zz_n, laundry_body()), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), flush=True)
