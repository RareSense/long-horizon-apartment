# final-sweep fix (AI-operated): bin walls rest on pouch r149 / papers r195i1 r195i3; their centres span 0.39 m along the bin's
# axis (> its 0.32 m footprint) so no push of the bin can enclose all four -> option 2: pick them out and drop them in again.
nm_ = "r149i1_pouch"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); o_ = {}
CK_STATE["item"] = "fix_" + nm_
print("ck", ck_save("x_fix_start", kind="act", info=dict(note="final-sweep fix start: re-drop pouch r149 / papers r195i3 r195i1 into the bin (AI-operated)")), "rec", rec.n, flush=True)
mon_start(target=pb_); MON["ignore_names"] = (pb_,)
try:
    try:
        pk_ = pick_floor(pb_, "auto")
    except RuntimeError as ex_:
        if "no place to stand" not in str(ex_):
            raise
        pk_ = with_tight(lambda: pick_floor(pb_, "auto"))
    o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
except Abort as ex_:
    o_["abort_pick"] = str(ex_)[:300]
except RuntimeError as ex_:
    o_["err_pick"] = str(ex_)[:300]
MON["on"] = False
print("PICK", o_, "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "pouch", np.round(centre(pb_), 3).tolist(), "bin", np.round(centre(bn_), 3).tolist(), "tilt", round(box_tilt_deg(bn_), 1), "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
print(look3("x01_pouch_pick"), flush=True)
