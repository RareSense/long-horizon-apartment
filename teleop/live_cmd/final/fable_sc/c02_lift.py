# AI-operated (Fable escalation, scooter r126): both jaws on the bar (checked). Checkpoint, then the skill's lift (3 cm stages).
print("ck", ck_save("fsc_gripped", kind="act", info=dict(note="scooter bar in both closed jaws, checked, not lifted (AI-operated)")), "rec", rec.n, flush=True)
mon_start(target=sc_); MON["t_max"] = 6000.0
try:
    st_ = sh_lift(sc_, say=lambda s_: print(s_, flush=True))
    print("LIFT", {k_: v_ for k_, v_ in st_.items()}, flush=True)
    print("seat", sh_seat(sc_), "on floor", sh_on_floor(sc_), flush=True)
    diag("lifted")
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
    diag("abort")
views("c02")
print("mem", mem(), flush=True)
