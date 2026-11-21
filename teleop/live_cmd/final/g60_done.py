# coat pile: final checks, then record the item (AI-operated)
t0_ = d.time
while not zz_w().asleep and d.time - t0_ < 6.0:
    op.run(0.5)
chk_ = in_container(zz_BL, zz_hb())
oth_ = {n_: item_check(n_) for n_ in ZZ_OTHERS}
own_ = item_check(zz_BL)
cr_ = contact_report()
print("coat", chk_, "asleep", bool(zz_w().asleep), flush=True)
print("item_check coat", own_, flush=True)
for n_, v_ in oth_.items():
    print(n_, v_, flush=True)
print("LOCK", dict(LOCK), "HELD", dict(HELD), "jaws", {s_: round(float(jaw(s_)), 4) for s_ in SIDES}, "fallen", fallen(), "touch", cr_, "state", state(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "route item", item_name(ROUTE[POS]), flush=True)
ok_ = bool(chk_["inside"] >= 0.9 and chk_["below_rim"] >= 0.9 and chk_["overhang"] < 0.06 and all(v_["ok"] for v_ in oth_.values()) and not LOCK and not HELD and not fallen() and cr_["body"] < 3.0)
print("ALL CRITERIA", ok_, flush=True)
if ok_:
    r_ = tele_item_done(zz_BL, note="AI-operated teleop (Fable): left hand, fingers down tilted 35 deg to the right and jaws fore-aft, slid in from the left onto BOTH hanging sleeves (one hold), lifted over the centre (all inside); both holds lowered in; right released fingers down-forward, left with steep fingers")
    print("ITEM DONE", r_, flush=True)
    print("frame", rec.n, flush=True)
    print("after: route item", item_name(ROUTE[POS]) if POS < len(ROUTE) else None, "DONE tail", DONE[-5:], "fallen", fallen(), "LOCK", dict(LOCK), "HELD", dict(HELD), flush=True)
    print("item checkpoints", sorted(n_ for n_ in os.listdir(CK_DIR) if "item_r116i1" in n_), flush=True)
print("look3", look3("g60_done"), flush=True)
