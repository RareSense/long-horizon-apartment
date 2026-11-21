zz_n = "r116i1_coat_pile"
BC["stage"] = "strand"
print("ck", ck_save("bc_coat_two_holds", kind="act"), flush=True)
zz_r = bigcloth_into(zz_n, s1="right", start="lift2", stop_after="lift2")
print("RESULT", zz_r, flush=True)
print("inside", in_container(zz_n, laundry_body()), "out", bc_out(zz_n, laundry_body()), "touch", contact_report(), "pads L/R rf", np.round(bc_to_rf(pad_mid("left")), 3).tolist(), np.round(bc_to_rf(pad_mid("right")), 3).tolist(), flush=True)
