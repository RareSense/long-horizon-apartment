# run bigcloth stages ZZ_START..ZZ_STOP for the coat (AI-operated)
print("ck", ck_save("g_before_" + ZZ_START, kind="act"), "frame", rec.n, flush=True)
zz_r = bigcloth_into(zz_BL, s1="right", start=ZZ_START, stop_after=ZZ_STOP)
for r_ in zz_r:
    print("RESULT", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:260]) for k_, v_ in r_.items() if k_ != "look"}, flush=True)
print("held L/R", cloth_held("left"), cloth_held("right"), "LOCK", {s_: len(LOCK[s_][1]) for s_ in LOCK}, "HELD", dict(HELD), "inside", in_container(zz_BL, zz_hb()), "out", zz_out_parts(), flush=True)
print("pads rf", {s_: np.round(zz_to_rf(pad_mid(s_)), 3).tolist() for s_ in SIDES}, "state", state(), "touch", contact_report(), "tilt", round(pelvis_tilt(), 3), "knees", zz_knees(), "fell", fallen(), flush=True)
print("others", zz_others(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), flush=True)
hc_ = obj_rect(zz_hb()).c
print("look", zz_look(np.array([hc_[0], hc_[1], 0.85]), "g56_" + ZZ_STOP, dist=1.4, h=0.6, dirs=(20.0, 160.0, 100.0), top=True), flush=True)
