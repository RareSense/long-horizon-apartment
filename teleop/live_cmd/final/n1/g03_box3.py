nm = "r175i1_cardboard_box"; b_ = body_of(nm)
ck_load(os.path.join(RUN, "checkpoints", [c_ for c_ in sorted(os.listdir(os.path.join(RUN, "checkpoints"))) if c_.endswith("_act_n1_box_part")][-1])); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
print("RELOADED box_part rec", rec.n, state(), "box", np.round(centre(b_), 3).tolist(), flush=True)
for stroke_ in range(3):
    if float(obj_box(b_)[1][1]) > 1.70 or fallen():
        break
    gap_ = float(obj_box(b_)[0][1]) - float(base()[0][1])
    if gap_ > 0.16:
        mon_start(target=None)
        try:
            tmove(fwd=float(min(0.10, gap_ - 0.14)), side=float(np.clip(-(base()[0][0] + 4.87), -0.04, 0.04)) * 0.0, tag=f"box_closer{stroke_}")
        except Abort as ex_:
            print("closer abort", ex_, flush=True)
        MON["on"] = False
    r_ = push_floor(nm, (0.0, 1.0), (-5.14, 0.0), 1.60, side="left", z=0.05)
    print("PUSH", stroke_, str(r_)[:500], "gap was", round(gap_, 3), "north face", round(float(obj_box(b_)[1][1]), 3), "pelvis", state()["pelvis"], flush=True)
    MON["on"] = False
print("box", np.round(centre(b_), 3).tolist(), "north face", round(float(obj_box(b_)[1][1]), 3), "tilt", round(box_tilt_deg(b_), 1), "state", state(), "fell", fallen(), flush=True)
print(look3("n1_box_end3"), flush=True)
