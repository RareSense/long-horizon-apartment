ck_load(os.path.join(RUN, "checkpoints", "3261_item_r149i1_pouch")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.3)); op.run(0.4)
rec.still_every = 300
nm = "r130i1_light_saber"; sb_ = body_of(nm); SD = "right"
print("RELOADED 3261 rec", rec.n, flush=True)
_start_item(nm)
gp_ = grasp_plan(sb_); opts_ = gp_.get("options") or [gp_]; c0_ = centre(sb_)
o_ = min(opts_, key=lambda o: float(np.linalg.norm(np.asarray(o["point"][:2]) - c0_[:2])))
cl_ = np.asarray(o_["closes"][0][:2], float); hs_ = [float(np.arctan2(cl_[1], cl_[0])) + s_ * np.pi / 2 for s_ in (-1, 1)]
yw_ = min(hs_, key=lambda h_: abs(wrapa(h_ - np.radians(-30.0))))
G_ = np.asarray(o_["point"], float); st_ = G_[:2] - RM.rz(yw_)[:2, :2] @ np.array([X_REL, -Y_REL])
print("grasp", np.round(G_, 3).tolist(), "closes", np.round(cl_, 3).tolist(), "stance", np.round(st_, 3).tolist(), round(float(np.degrees(yw_)), 1), "top", round(float(o_.get("top", G_[2] + 0.02)), 3), flush=True)
out_ = {}
mon_start(target=sb_)
try:
    walk_tight((float(st_[0]), float(st_[1]), float(yw_)))
    print("ck", ck_save("n1_saber_stance", kind="act", info=dict(note="saber pick stance (AI-operated)")), flush=True)
    open_jaws(SD, T=0.3)
    PRE_ACTION("crouch", dict(CROUCH)); crouch(T=1.8, **CROUCH)
    Q_ = {SD: q_(R_down(np.r_[cl_, 0.0]))}
    PRE_ACTION("servo_pads", {}); out_["e_above"] = np.round(servo_pads(SD, G_[:2], float(G_[2]) + 0.08, Q_, speed=0.15), 3).tolist()
    PRE_ACTION("servo_pads", {}); out_["e_down"] = np.round(servo_pads(SD, G_[:2], float(G_[2]) + 0.004, Q_, speed=0.05, n=3), 3).tolist()
    out_["pad"] = np.round(pad_mid(SD), 3).tolist(); out_["ahead"] = round(ahead_of_pelvis(pad_mid(SD)), 3)
    PRE_ACTION("close_jaws", {}); close_jaws(SD, 10.0, T=0.8)
    g_ = grip_check(SD, sb_, min_gap=0.004); out_["grip"] = {k: g_[k] for k in g_ if k in ("ok", "gap", "jaw1_N", "jaw2_N")}; out_["fingers"] = len(jaw_fingers_on(SD, sb_))
    if g_["ok"] and hold_on(SD, sb_):
        HELD[SD] = dict(min_gap=0.004); MON["held"][SD] = sb_; MON["target"] = None; MON["last_touch"][SD] = float(d.time)
        z0_ = float(centre(sb_)[2]); hp_ = ts.ee_pose(SD)[0]
        PRE_ACTION("lift", {}); op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.10]}, speed=0.05, quats=Q_, timeout=3.0, tol=0.008); op.run(0.3)
        out_["rose"] = round(float(centre(sb_)[2]) - z0_, 3); out_["held"] = not hold_lost(SD)
except (Abort, RuntimeError) as ex_:
    out_["abort"] = str(ex_)[:300]
MON["on"] = False
print("SABER", out_, "at", np.round(centre(sb_), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print(look_hand(SD, "n1_saber_grip"), flush=True)
