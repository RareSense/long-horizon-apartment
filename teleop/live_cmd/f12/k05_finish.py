MON["on"] = False
bk_ = body_of("r186i1_basket")
print("nugget", np.round(centre(zz_b), 3).tolist(), "in basket", inside(zz_b, bk_), flush=True)
hp_ = pad_mid(SD)
PRE_ACTION("hand_up", {}); servo_pads(SD, hp_[:2], hp_[2] + 0.10, QB, speed=0.08, n=1)
PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2)
rest_hands(SIDES, T=0.6)
print("state", state(), "fell", fallen(), "touch", contact_report()["body"], "in basket", inside(zz_b, bk_), flush=True)
if inside(zz_b, bk_) and not fallen():
    print("DONE", item_done_auto("r93i1_nugget", dict(status="done", how="surface pick by AI teleop (level hand, fingers forward, jaws sideways) at the island edge after the library's top-down pick could not reach; first basket drop missed (hand 31 cm short: it fell beside the basket); library pick_floor, then the basket stance (-4.85,-1.05,-125 deg) with a deep squat, hand checked over the basket, released (AI-operated)")), flush=True)
print(look3("f12_nugget_done"), flush=True)
