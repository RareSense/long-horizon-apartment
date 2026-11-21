# final checks, then record the item (AI-operated)
t0_ = d.time
while not zz_w().asleep and d.time - t0_ < 6.0:
    op.run(0.5)
chk_ = in_container(zz_BL, zz_hb())
oth_ = {n_: item_check(n_) for n_ in ("r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket")}
own_ = item_check(zz_BL)
cr_ = contact_report()
print("blanket", chk_, "asleep", bool(zz_w().asleep), flush=True)
print("item_check blanket", own_, flush=True)
for n_, v_ in oth_.items():
    print(n_, v_, flush=True)
print("LOCK", dict(LOCK), "HELD", dict(HELD), "jaws", {s_: round(float(jaw(s_)), 4) for s_ in SIDES}, "fallen", fallen(), "touch", cr_, "state", state(), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), "route item", item_name(ROUTE[POS]), flush=True)
ok_ = bool(chk_["inside"] >= 0.9 and chk_["below_rim"] >= 0.9 and chk_["overhang"] < 0.06 and all(v_["ok"] for v_ in oth_.values()) and not LOCK and not HELD and not fallen() and cr_["body"] < 3.0)
print("ALL CRITERIA", ok_, flush=True)
if ok_ and globals().get("ZZ_RECORD"):
    r_ = tele_item_done(zz_BL, note="AI-operated teleop (Fable): left hand took the near fold of the hanging strand (fingers ahead, jaws side by side), lifted over the centre; right let go fingers-down; right re-took the sagging far end + first-end edge above the north handle and lifted the last corner over the rim; both lowered in, released with steep fingers")
    print("ITEM DONE", r_, flush=True)
    print("frame", rec.n, flush=True)
print("look3", look3("g42_done"), flush=True)
hc_ = obj_rect(zz_hb()).c
print("look", zz_look(np.array([hc_[0], hc_[1], 0.5]), "g42_done", dist=1.3, h=0.8, dirs=(20.0, 160.0), top=True), flush=True)
