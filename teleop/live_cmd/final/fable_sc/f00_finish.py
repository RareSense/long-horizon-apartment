# AI-operated (Fable escalation, scooter r126): record the item. _finish checks the item's place BEFORE item_done_auto writes
# the new spot, so the spot given for this item (-2.20, 0.0, floor) is written first (the same two lines item_done_auto
# runs), then _finish as asked.
sh_recentre.__defaults__ = (0.30, 0.025, 0.03)
print("route at", item_name(ROUTE[POS]), "POS", POS, "done already", nm in DONE, "item", CK_STATE.get("item"), flush=True)
print("check before", item_check(nm), flush=True)
OVR["dest"][nm] = "floor"; OVR["spots"][nm] = [-2.20, 0.0]; apply_ovr()
c_ = item_check(nm)
print("check with the spot", c_, "fallen", fallen(), "held", _held_any(), flush=True)
if c_.get("ok") and not fallen() and not _held_any():
    print("FIN", _finish(nm, "Fable escalation, AI-operated teleop with park_scooter_hang's own sh_* steps: take stance 12 cm further back, open hands "
                             "behind the bar, a 7 cm step in, grip, lift; carried hanging 12 moves (turns with side steps round the fan and basket, "
                             "backward north); 4 set-down legs to tilt 4.4 deg, then both squeezes eased to 6 N so the bar left the pads and the scooter "
                             "came down onto its front wheels; release, 2 side steps, 2 steps back", spot=(-2.20, 0.0)), flush=True)
else:
    print("NOT RECORDED", flush=True)
print("POS", POS, "next", item_name(ROUTE[POS]) if POS < len(ROUTE) else None, "state", state(), "rec", rec.n, "mem", mem(), flush=True)
