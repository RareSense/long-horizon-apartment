CARRY_JOINTS = False
t0_ = d.time
while not zz_w().asleep and d.time - t0_ < 10.0:
    op.run(0.5)
print("asleep", bool(zz_w().asleep), "awake garments", cloth_awake(), "quiet", ck_quiet(), "ARM_NOW", ARM_NOW, "HELD", dict(HELD), "LOCK", dict(LOCK), "SQ", list(SQ), flush=True)
zz_chk = in_container(zz_BL, zz_hb())
print("blanket", zz_chk, "state", state(), "tilt", round(pelvis_tilt(), 3), "touch", contact_report(), "disk", ck_disk(), flush=True)
assert zz_chk["inside"] >= 0.9 and zz_chk["below_rim"] >= 0.9 and zz_chk["overhang"] < 0.06 and not fallen() and not LOCK and not HELD
for e_ in CK_LOG:                      # the named teleop checkpoints of this escalation stay (for a replay)
    if str(e_.get("name", "")).startswith("fb_") and e_.get("pruned") is None:
        e_["pruned"] = False
zz_done = tele_item_done("r117i1_blanket", note="ESCALATION (Fable, AI-operated teleop): right-hand grasp at the west edge middle, front stance north of the hamper, hand-over-hand over the rim (left hand on the taut strand, right hand on the fold outside the rim), both holds lifted over the opening, lowered and let go. inside 1.0, below the rim 1.0; nothing knocked.")
print("ITEM DONE", zz_done, flush=True)
print("route head now", [item_name(s_) for s_ in ROUTE[POS:POS + 4]], "done", DONE, "disk", ck_disk(), flush=True)
