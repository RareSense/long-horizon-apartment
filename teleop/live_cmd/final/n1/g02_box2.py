nm = "r175i1_cardboard_box"; b_ = body_of(nm)
print("ck", ck_save("n1_box_part", kind="act", info=dict(note="box pushed 5 cm (one stroke) (AI-operated)")), flush=True)
mon_start(target=None)
try:
    walk_tight((-5.0, 1.13, np.pi / 2))
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("stance", state(), "box lo y", round(float(obj_box(b_)[0][1]), 3), flush=True)
for stroke_ in range(2):
    if float(obj_box(b_)[1][1]) > 1.70 or fallen():
        break
    gap_ = float(obj_box(b_)[0][1]) - float(base()[0][1])
    if stroke_ > 0 and gap_ > 0.16:
        mon_start(target=None)
        try:
            tmove(fwd=float(min(0.10, gap_ - 0.14)), tag=f"box_closer{stroke_}")
        except Abort as ex_:
            print("closer abort", ex_, flush=True)
        MON["on"] = False
    r_ = push_floor(nm, (0.0, 1.0), (-5.20, 0.0), 1.60, side="left", z=0.05)
    print("PUSH", stroke_, str(r_)[:500], "gap was", round(gap_, 3), "north face", round(float(obj_box(b_)[1][1]), 3), flush=True)
    MON["on"] = False
print("box", np.round(centre(b_), 3).tolist(), "north face", round(float(obj_box(b_)[1][1]), 3), "tilt", round(box_tilt_deg(b_), 1), "state", state(), "fell", fallen(), flush=True)
print(look3("n1_box_end2"), flush=True)
