# rug toys r193i1 / r193i3 set aside (NOT route items; they go into the toy basket later), as the first chain did before
# the garments: every hamper drop stance was limited by them. AI-operated.
CK_STATE["item"] = f"{POS + 1:03d}_aside_rug_toys"
for nm_, sp_ in (("r193i1_toy_piece", (-2.927, -0.581)), ("r193i3_toy_piece", (-2.79, -0.605))):
    print("before", nm_, np.round(centre(body_of(nm_)), 3).tolist(), flush=True)
    r_ = set_aside(nm_, sp_)
    print("ASIDE", {k_: v_ for k_, v_ in r_.items() if k_ != "look"}, flush=True)
    print("after", nm_, np.round(centre(body_of(nm_)), 3).tolist(), "state", state(), "held", {s_: HOLD.holding(s_) for s_ in SIDES}, "fell", fallen(), flush=True)
    if r_.get("status") != "done":
        break
    print("CK", ck_save(f"aside_{nm_}", kind="item", info=dict(aside=True, note="set aside (not a route item), AI-operated")), flush=True)
print(look3("asides_end"), flush=True)
