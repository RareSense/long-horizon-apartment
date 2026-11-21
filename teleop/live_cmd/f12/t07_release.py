o_ = {}
mon_start(target=SB); MON["held"] = {}; MON["t_max"] = 6000.0
try:
    for s_ in SIDES:
        ts.ctrl.ext.pop(f"hold_{s_}", None)
        try:
            ts.setup.end_effectors[s_].pop("rot_weight", None)
        except Exception:
            pass
    for s_ in SIDES:
        jaw_force[s_] = 20.0; jaw_target[s_] = JAW_OPEN
    op.run(0.6)
    p_, y_ = base()
    for (ah_, sd_, z_) in ((0.18, 0.30, 1.15), (0.12, 0.30, 0.95), (0.05, 0.30, 0.70)):
        tg_ = {s_: (np.r_[p_[:2] + RM.rz(y_)[:2, :2] @ np.array([ah_, (1.0 if s_ == "left" else -1.0) * sd_]), z_]).tolist() for s_ in SIDES}
        PRE_ACTION("hands_off_bar", dict(to=[ah_, sd_, z_]))
        op.move(tg_, speed=0.10, timeout=4.0, tol=0.03); op.run(0.2)
    rest_hands(SIDES, T=1.0); op.run(0.6)
    o_["box_after_hands"] = [np.round(v_, 3).tolist() for v_ in obj_box(SB)]
    for kw_ in (dict(fwd=-0.15), dict(fwd=-0.15), dict(side=0.15), dict(side=0.15)):
        tmove(tag="sc_off", **kw_)
        if MON.get("why"):
            raise Abort(MON["why"])
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
lo_, hi_ = obj_box(SB)
o_.update(box=[np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist()], tilt=sh_state(SB)["tilt"], on_floor=len(sh_on_floor(SB)), state=state(), fell=fallen())
print("REL", o_, flush=True)
moved_ = []
for b_, p0_ in (MON.get("start") or {}).items():
    if b_ == SB:
        continue
    dp_ = float(np.linalg.norm(d.xpos[m.body(b_).id][:2] - p0_[:2]))
    if dp_ > 0.01:
        moved_.append((INFO["bodies"].get(b_, {}).get("display"), round(dp_, 3)))
print("moved since release start", moved_, flush=True)
print(look3("f12_scooter_parked"), flush=True)
