ck_load(os.path.join(RUN, "checkpoints", "0364_item_r190i1_stocking")); gait_on(); settle_after_load()
print("loaded", state(), "route at", item_name(ROUTE[POS]), flush=True)
for b_ in INFO["bodies"]:
    c_ = centre(b_)
    if -5.1 < c_[0] < -4.4 and -0.9 < c_[1] < 0.2:
        print("thing", INFO["bodies"][b_].get("display", b_), np.round(c_, 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(b_)], flush=True)
