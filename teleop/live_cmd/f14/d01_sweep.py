# Final sweep over ALL done items (AI-operated): is each really at its destination now?
import json as _js
SWEEP = []
seen_ = []
for nm_ in DONE:
    if nm_ in seen_:
        continue
    seen_.append(nm_)
    r_ = dict(item=nm_)
    try:
        if nm_ in ("scene_removed_40",) or nm_.startswith("start"):
            r_.update(kind="meta", ok=None); SWEEP.append(r_); continue
        if nm_.endswith("_door") or "door" in nm_ and "dishwasher" not in nm_:
            A_, ax_, a_, bid_, j_ = hinge_axis(nm_)
            q_ = float(d.qpos[a_]); rg_ = m.jnt_range[j_]; qg_ = float(rg_[0]) if abs(float(rg_[0])) > abs(float(rg_[1])) else float(rg_[1])
            r_.update(kind="door", q=round(q_, 3), shut_end=round(qg_, 3), ok=bool(abs(q_ - qg_) < np.radians(3.0))); SWEEP.append(r_); continue
        if "dishwasher" in nm_:
            r_.update(kind="dishwasher", ok=None, note="check by joints below"); SWEEP.append(r_); continue
        b_ = body_of(nm_)
        disp_ = INFO["bodies"].get(b_, {}).get("display", nm_) if b_ else nm_
        if "GARMENTS" in globals() and (disp_ in GARMENTS or nm_ in GARMENTS):
            gk_ = disp_ if disp_ in GARMENTS else nm_
            dest_ = place_for(b_) if b_ else None
            ic_ = in_container(gk_, dest_) if (dest_ and dest_ in INFO["bodies"] and "in_container" in globals()) else None
            r_.update(kind="garment", body=b_, dest=dest_, in_container=ic_, ok=bool(ic_ and ic_["inside"] > 0.8) if ic_ else None)
            SWEEP.append(r_); continue
        dest_ = place_for(b_); sp_ = spot_of(b_)
        c_ = centre(b_); lo_, hi_ = obj_box(b_)
        ok_ = at_place(b_)
        r_.update(kind="thing", body=b_, dest=dest_, spot=None if sp_ is None else np.round(sp_, 3).tolist(), centre=np.round(c_, 3).tolist(), low_z=round(float(lo_[2]), 3),
                  ok=bool(ok_), touching=sorted(set(_thing_contacts(b_)))[:6] if "_thing_contacts" in globals() else None)
        if dest_ == "floor" and sp_ is not None:
            r_["off_spot"] = round(float(np.linalg.norm(c_[:2] - np.asarray(sp_)[:2])), 3)
    except Exception as ex_:
        r_.update(ok=None, err=str(ex_)[:160])
    SWEEP.append(r_)
for r_ in SWEEP:
    print("SW", r_, flush=True)
print("N", len(SWEEP), "ok", sum(1 for r_ in SWEEP if r_.get("ok") is True), "NOT", [r_["item"] for r_ in SWEEP if r_.get("ok") is False], "unknown", [r_["item"] for r_ in SWEEP if r_.get("ok") is None], flush=True)
print("SPOT_TOL", globals().get("SPOT_TOL"), "OVR", str(OVR)[:800], flush=True)
_js.dump(SWEEP, open(os.path.join(RUN, "final_sweep.json"), "w"), indent=1, default=str)
