zz_hb = body_of("r133i1_laundry_basket"); zz_lo, zz_hi = obj_box(zz_hb)
print("hamper box", np.round(zz_lo, 3).tolist(), np.round(zz_hi, 3).tolist())
zz_hat = body_of("r131i1_knit_hat")
try:
    print("hat box", [np.round(x, 3).tolist() for x in obj_box(zz_hat)])
except Exception as e_:
    print("hat box err", e_)
print("held", MON.get("held"), "HELD", {k: str(v)[:80] for k, v in HELD.items()})
print("state", state())
print("touch", contact_report() if "contact_report" in globals() else None)
print("look", look_hand("left", "insp_left"), flush=True)
zz_ck = sorted(os.listdir(os.path.join(RUN, "checkpoints")))
print("last ckpts", zz_ck[-8:], flush=True)
