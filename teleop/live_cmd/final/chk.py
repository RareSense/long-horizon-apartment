# Item-end destination check (coordinator): run before EVERY item checkpoint; the checkpoint is NOT saved when the
# item is not at its destination (prints CHECK_FAIL; fix it, then save with route_checkpoint(nm) by hand). AI-operated.
CHECKS = globals().get("CHECKS", [])


def item_check(nm_):
    r_ = dict(item=nm_, t=round(float(d.time), 2))
    try:
        if nm_.startswith("start") or nm_ in ("scene_removed_40",):
            r_.update(kind="meta", ok=True); return r_
        if nm_ == "close_dishwasher":
            qs_ = {}
            for dn_ in ("r32i1_door",):
                A_, ax_, a_, bid_, j_ = hinge_axis(dn_)
                q_ = float(d.qpos[a_]); rg_ = m.jnt_range[j_]; qg_ = float(rg_[0]) if abs(float(rg_[0])) > abs(float(rg_[1])) else float(rg_[1])
                qs_[dn_] = (round(q_, 3), round(qg_, 3))
            r_.update(kind="dishwasher", q=qs_, ok=all(abs(a - b) < np.radians(3.0) for a, b in qs_.values())); return r_
        if nm_.endswith("_door"):
            A_, ax_, a_, bid_, j_ = hinge_axis(nm_)
            q_ = float(d.qpos[a_]); rg_ = m.jnt_range[j_]; qg_ = float(rg_[0]) if abs(float(rg_[0])) > abs(float(rg_[1])) else float(rg_[1])
            r_.update(kind="door", q=round(q_, 3), shut_end=round(qg_, 3), ok=bool(abs(q_ - qg_) < np.radians(3.0))); return r_
        b_ = body_of(nm_)
        disp_ = INFO["bodies"].get(b_, {}).get("display", nm_) if b_ else nm_
        if "GARMENTS" in globals() and (disp_ in GARMENTS or nm_ in GARMENTS):
            gk_ = disp_ if disp_ in GARMENTS else nm_
            dest_ = place_for(b_) if b_ else (DESC["destinations"].get(gk_) or DESC["destinations"].get(nm_))
            ic_ = in_container(gk_, dest_) if (dest_ and dest_ in INFO["bodies"] and "in_container" in globals()) else None
            r_.update(kind="garment", dest=dest_, inside=None if not ic_ else round(float(ic_["inside"]), 3), ok=bool(ic_ and ic_["inside"] > 0.8) if ic_ else None)
            return r_
        dest_ = place_for(b_); sp_ = spot_of(b_)
        c_ = centre(b_)
        r_.update(kind="thing", dest=dest_, centre=np.round(c_, 3).tolist(), ok=bool(at_place(b_)))
        if sp_ is not None:
            r_["off_spot"] = round(float(np.linalg.norm(c_[:2] - np.asarray(sp_)[:2])), 3)
            if dest_ == "floor":
                r_["ok"] = bool(r_["off_spot"] <= SPOT_TOL)
        if dest_ and dest_ in INFO["bodies"]:
            r_["inside"] = bool(inside(b_, dest_))
    except Exception as ex_:
        r_.update(ok=None, err=str(ex_)[:200])
    return r_


if "_route_checkpoint_raw" not in globals():
    _route_checkpoint_raw = route_checkpoint


def route_checkpoint(name, force=False):
    r_ = item_check(name)
    CHECKS.append(r_)
    print("ITEM_CHECK", r_, flush=True)
    if r_.get("ok") is False and not force:
        print("CHECK_FAIL: item checkpoint NOT saved for", name, "- fix it, then route_checkpoint(name) (or force=True with a reason)", flush=True)
        return None
    return _route_checkpoint_raw(name)


def say_item(nm_=None):
    """The last item checkpoint + done count, for the per-item message."""
    cks_ = [c_ for c_ in sorted(os.listdir(CK_DIR)) if "_item_" in c_]
    return dict(done=len(DONE), last=os.path.join(CK_DIR, cks_[-1]) if cks_ else None, next=item_name(ROUTE[POS]) if POS < len(ROUTE) else None, frame=rec.n, t=round(float(d.time), 1), kit=kit_mem())


print("[chk] item_check + guarded route_checkpoint loaded; SPOT_TOL", SPOT_TOL, flush=True)
