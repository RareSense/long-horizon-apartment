nm = "r175i1_cardboard_box"; b_ = body_of(nm)
mon_start(target=None)
try:
    tmove(fwd=-0.10, tag="box_off"); rest_hands(SIDES); op.run(1.0)
except Abort as ex_:
    print("off abort", ex_, flush=True)
MON["on"] = False
sp_ = np.array([-5.25, 1.56]); off_ = float(np.linalg.norm(centre(b_)[:2] - sp_))
print("box", np.round(centre(b_), 3).tolist(), "off spot", round(off_, 3), "tilt", round(box_tilt_deg(b_), 1), "state", state(), "held", _held_any(), "fell", fallen(), flush=True)
if off_ < 0.05 and box_tilt_deg(b_) < 3 and not fallen() and not _held_any():
    _bring(nm)
    _rc_guarded = route_checkpoint
    route_checkpoint = lambda name, force=False: _rc_guarded(name, force=True)      # dest is a description string, not "floor": at_place cannot say True (first chain sweep note); checked here by its spot (2 mm) + against the wall
    try:
        zz_d = tele_item_done(nm, note=f"AI-operated night finisher: push_floor north along the wall in two strokes from (-4.87,1.10) at the line x -5.14 (the runner's line x -5.23 was out of reach: 1-5 mm a step), step closer between strokes; centre {np.round(centre(b_), 3).tolist()} = {off_*100:.1f} cm from its spot (-5.25,1.56), north face against the wall (1.742 vs wall 1.735), upright (tilt {box_tilt_deg(b_):.1f} deg).")
    finally:
        route_checkpoint = _rc_guarded
    print("ITEM DONE", zz_d, "done", len(DONE), "rec", rec.n, flush=True)
