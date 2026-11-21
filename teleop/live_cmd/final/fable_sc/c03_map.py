# AI-operated (Fable escalation, scooter r126): lifted. Checkpoint; what stands round the route (no motion).
print("ck", ck_save("fsc_lifted", kind="act", info=dict(note="scooter hangs from the bar in both jaws at carry height (AI-operated)")), "rec", rec.n, flush=True)
bid_ = m.body(sc_).id
for b_ in range(1, m.nbody):
    n_ = m.body(b_).name
    if b_ == bid_ or "link" in n_ or n_ in ("pelvis", "world", "scene_static"):
        continue
    try:
        lo_, hi_ = obj_box(n_)
    except Exception:
        continue
    if hi_[0] > -3.2 and lo_[0] < -0.8 and hi_[1] > -2.3 and lo_[1] < 1.0 and hi_[2] > 0.02:
        print("  near", n_, INFO["bodies"].get(n_, {}).get("display", "") if isinstance(INFO.get("bodies"), dict) else "", np.round(lo_, 2).tolist(), np.round(hi_, 2).tolist(), flush=True)
try:
    g_ = room_grid((sc_,))
    rr_ = [r_ for r_ in g_.rects if r_[2] > -3.2 and r_[0] < -0.8 and r_[3] > -2.3 and r_[1] < 1.0]
    print("grid rects (x0,y0,x1,y1...) n", len(rr_), flush=True)
    for r_ in rr_:
        print("  rect", np.round(np.asarray(r_[:4], float), 2).tolist(), r_[4:] if len(r_) > 4 else "", flush=True)
except Exception as ex_:
    print("grid:", str(ex_)[:200], flush=True)
pth_ = os.path.join(TELE_DIR, "fsc_c03_map.jpg"); close(pth_, np.array([-1.95, -0.45, 4.6]), np.array([-1.95, -0.40, 0.0]), "AI-operated | route area from above (north up?)")
print("MAP", pth_, flush=True)
