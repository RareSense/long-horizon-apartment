mon_start(target=None); MON["ignore_names"] = (zz_cb, body_of("r130i1_light_saber"), zz_b)
try:
    thand("right", dx=-0.04, tag="duck_hand_back"); rest_hands(SIDES, T=0.8); op.run(0.4)
    r_ = tmove(fwd=-0.10, tag="off_saber"); print("off", r_["at"], r_["touch"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("saber pieces", {k_: np.round(V_.mean(0), 3).tolist() for k_, V_ in piece_points(body_of("r130i1_light_saber")).items()}, "duck in", inside(zz_b, zz_cb), "stocking", in_container("r190i1_stocking", zz_cb)["inside"], "state", state(), "touch", contact_report(), flush=True)
print(look3("duck_done"), flush=True)
