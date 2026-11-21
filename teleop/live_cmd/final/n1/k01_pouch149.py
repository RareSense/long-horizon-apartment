rec.still_every = 300
nm = "r149i1_pouch"; pb_ = body_of(nm)
_start_item(nm)
cands_ = []
for k_ in range(4):
    for sd_ in SIDES:
        for p_ in corner_pinch_plan(pb_, k_, sd_, 0.018):
            if p_["free"]:
                cands_.append((float(np.linalg.norm(np.asarray(p_["stance"][:2]) - base()[0][:2])), k_, sd_, p_))
cands_.sort(key=lambda c_: c_[0]); _, KK, SDP, pl_ = cands_[0]
print("cands", [(round(c_[0], 2), c_[1], c_[2], np.round(c_[3]["stance"], 3).tolist()) for c_ in cands_], flush=True)
print("plan", np.round(pl_["stance"], 3).tolist(), "free", pl_["free"], flush=True)
mon_start(target=pb_)
try:
    walk_tight(pl_["stance"])
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("at stance", state(), "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
print("ck", ck_save("n1_pouch149_stance", kind="act", info=dict(note="table corner stance for pouch r149 (AI-operated)")), flush=True)
try:
    crouch(*surface_posture(0.47), T=1.2)
except Exception as ex_:
    print("posture ERR", str(ex_)[:150], flush=True)
c_ = corner_pick(nm, SDP); print("CORNER", {k_: v_ for k_, v_ in c_.items() if k_ != "Q"}, flush=True)
if c_.get("held"):
    print("ck", ck_save("n1_pouch149_held", kind="act", info=dict(note="pouch r149 held (corner pinch, guarded) (AI-operated)")), flush=True)
    _to_bin(nm, SDP)
print("pouch", np.round(centre(pb_), 3).tolist(), "check", item_check(nm), "state", state(), "fell", fallen(), flush=True)
print("FIN", _finish(nm, "AI-operated night finisher: walk to the table-corner stance (corner 1, left), surface_posture, corner_pick 1.8 cm in (guarded hold), bin_drop"), flush=True)
print(look3("n1_pouch149_end"), flush=True)
