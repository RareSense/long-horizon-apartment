MON["on"] = False
nm_ = "r193i1_toy_piece"; zz_b = body_of(nm_); SD = "left"; bk_ = body_of("r186i1_basket"); o_ = {}
Rn_ = ts.ee_pose(SD)[1]; cd_ = Rn_[:, 1].copy(); cd_[2] = 0; cd_ /= np.linalg.norm(cd_); QB = {SD: q_(R_down(cd_))}
mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
try:
    PRE_ACTION("stand_with", {}); squat_follow((SD,), -0.20, 0.35); crouch_holding((SD,), 0.0, 0.0, T=1.5)
    o_["held_stand"] = not hold_lost(SD)
    over_ = np.array([-5.13, -1.39])
    p_, y_ = base(); R2_ = RM.rz(y_)[:2, :2]
    rel_ = R2_.T @ (over_ - p_[:2])
    # put the basket middle 0.36 ahead and 0.20 to the left of the standing pelvis (left hand reach in the squat)
    mv_ = rel_ - np.array([0.36, 0.20])
    o_["move"] = np.round(mv_, 3).tolist()
    tmove(fwd=float(mv_[0]), side=float(mv_[1]), carry=(SD,), tag="basket_left")
    PRE_ACTION("squat", {}); squat_follow((SD,), -0.20, 0.35); squat_follow((SD,), -0.30, 0.6)
    e_ = servo_pads(SD, over_, 0.30, QB, speed=0.06)
    if np.linalg.norm(e_[:2]) > 0.04:
        PRE_ACTION("squat_deep", {}); squat_follow((SD,), -0.38, 0.8); e_ = servo_pads(SD, over_, 0.30, QB, speed=0.06)
    o_["e_over"] = np.round(e_, 3).tolist()
    if np.linalg.norm(e_[:2]) < 0.07:
        MON["ignore_names"] = tuple(set(MON.get("ignore_names", ())) | {zz_b}); MON["start"].pop(zz_b, None)
        PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(0.8)
    hp_ = pad_mid(SD)
    PRE_ACTION("hand_up", {}); servo_pads(SD, hp_[:2], hp_[2] + 0.10, QB, speed=0.08, n=1)
    PRE_ACTION("stand", {}); crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(inside=inside(zz_b, bk_), held=HOLD.holding(SD), state=state(), fell=fallen())
print("FIX", o_, flush=True)
if o_["inside"] and not o_["fell"]:
    print("DONE", item_done_auto(nm_, dict(status="done", how="library pick_floor; basket put with the LEFT hand stopped 0.30 m short at the right-hand stance; stood up holding, stepped so the basket lay 0.36 ahead / 0.20 left, squat, hand checked over the basket, released (AI-operated)")), flush=True)
print(look3("f12_r193i1_fix"), flush=True)
