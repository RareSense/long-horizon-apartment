zz_n = "r116i1_coat_pile"
zz_r = bigcloth_into(zz_n, s1="right", start="first_end", stop_after="first_end")
print("RESULT", zz_r, flush=True)
print("inside", in_container(zz_n, laundry_body()), "out", bc_out(zz_n, laundry_body()), "touch", contact_report(), "strand target", bc_strand_target(zz_n, laundry_body(), "left"), flush=True)
