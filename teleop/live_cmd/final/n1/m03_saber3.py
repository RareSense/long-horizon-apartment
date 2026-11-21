ck_load(os.path.join(RUN, "checkpoints", "3261_item_r149i1_pouch")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.3)); op.run(0.4)
rec.still_every = 300
print("RELOADED 3261 rec", rec.n, state(), flush=True)
nm = "r130i1_light_saber"; sb_ = body_of(nm)
_ps0 = pick_stance
_ps_used = {"n": 0}
def pick_stance(name, side="auto"):
    if name != sb_ or _ps_used["n"] > 0:
        return _ps0(name, side)
    _ps_used["n"] += 1
    gp_ = grasp_plan(name)
    opts_ = gp_.get("options") or [gp_]
    c_ = centre(name)
    o_ = min(opts_, key=lambda o: float(np.linalg.norm(np.asarray(o["point"][:2]) - c_[:2])))
    cl_ = np.asarray(o_["closes"][0][:2], float) if o_.get("closes") else np.array([-0.75, 0.66])
    hs_ = [float(np.arctan2(cl_[1], cl_[0])) + s_ * np.pi / 2 for s_ in (-1, 1)]
    yw_ = min(hs_, key=lambda h_: abs(wrapa(h_ - np.radians(150.0))))
    g_ = np.asarray(o_["point"][:2], float) - RM.rz(yw_)[:2, :2] @ np.array([X_REL, Y_REL])
    print("FORCED saber stance", np.round(g_, 3).tolist(), round(float(np.degrees(yw_)), 1), "point", np.round(o_["point"], 3).tolist(), flush=True)
    return (float(g_[0]), float(g_[1]), float(yw_)), "left", o_
try:
    zz_ok = _pick_put_floor("r130i1_light_saber", (-4.92, -1.405), 0, side="left")
except Exception:
    import traceback as _tb; print("EXC", _tb.format_exc()[-1200:], flush=True); zz_ok = False
finally:
    pick_stance = _ps0
print("ZZ_OK", zz_ok, "saber", np.round(centre(sb_), 3).tolist(), "check", item_check(nm), "state", state(), "fell", fallen(), "rec", rec.n, flush=True)
