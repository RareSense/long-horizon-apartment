rec.still_every = 300
nm = "r126i1_scooter"; sc_ = body_of(nm)
_start_item(nm)
mon_start(target=None)
try:
    walk_tight((-2.0, 1.0, -1.47))
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
print("pre", state(), "scooter", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], flush=True)
print("ck", ck_save("n1_scooter_pre", kind="act", info=dict(note="scooter call start pose (-2.0,1.0) facing south (AI-operated)")), flush=True)
_x(r"E:\urc_final\scripts\home\live\scooter_hang.py")
r_ = park_scooter_hang(nm)
print("SCOOTER", {k_: v_ for k_, v_ in r_.items() if k_ not in ("moves",)}, flush=True)
print("FIN", _finish(nm, "park_scooter_hang (Fable's one call) from (-2.0,1.0) facing south", spot=(-2.20, 0.0)) if r_.get("status") == "done" else False, flush=True)
