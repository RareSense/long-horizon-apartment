MON["on"] = False
ck_load(os.path.join(RUN, "checkpoints", "0182_item_r125i1_flat")); gait_on(); settle_after_load(); refresh_jointed_footprints()
for n_ in ("r101i1_stroller", "r102i1_tote", "r106i1_umbrella", "r107i1_umbrella", "r105i1_shoe", "r105i2_shoe", "r120i1_duck"):
    b_ = body_of(n_)
    print(n_, b_, "loose" if b_ in INFO["bodies"] else "STATIC", [np.round(v_, 2).tolist() for v_ in obj_box(b_)] if b_ in INFO["bodies"] else [s_.get("boxes", [{}])[0].get("c") for s_ in INFO["static"] if s_["name"].startswith(n_[:4])][:2], DESC["destinations"].get(n_), flush=True)
