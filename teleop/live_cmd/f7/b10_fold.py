zz_n = "r116i1_coat_pile"
zz_r = bigcloth_into(zz_n, s1="right", start="fold", stop_after="fold")
print("RESULT", zz_r, flush=True)
print("inside", in_container(zz_n, laundry_body()), "out", bc_out(zz_n, laundry_body()), "held L/R", cloth_held("left"), cloth_held("right"), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "fold look", BC.get("fold_look"), flush=True)
