zz_n = "r116i1_coat_pile"
print("between pads now", len(bc_w(zz_n).caught("left")), "pad rf", np.round(bc_to_rf(pad_mid("left")), 3).tolist(), "tgt rf", np.round(bc_to_rf(bc_w(zz_n).points(0)[1823]), 3).tolist(), flush=True)
zz_c = bc_close_lock(zz_n, "left")
print("close", zz_c, "held L/R", cloth_held("left"), cloth_held("right"), flush=True)
if zz_c["caught"]:
    hu_ = bc_uv(zz_n)[LOCK["left"][1]]
    print("left held uv lo/hi", np.round(hu_.min(0), 2).tolist(), np.round(hu_.max(0), 2).tolist(), "right held uv", np.round(bc_uv(zz_n)[LOCK["right"][1]].mean(0), 2).tolist(), flush=True)
print("look", look_hand("left", "bc_strand_closed"), flush=True)
