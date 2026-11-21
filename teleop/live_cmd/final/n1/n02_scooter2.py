rec.still_every = 300
nm = "r126i1_scooter"; sc_ = body_of(nm)
ck_load(os.path.join(RUN, "checkpoints", "3697_act_n1_scooter_pre")); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.5)
print("RELOADED 3697 rec", rec.n, state(), flush=True)
_x(r"E:\urc_final\scripts\home\live\scooter_hang.py")
r_ = park_scooter_hang(nm)
print("SCOOTER", {k_: v_ for k_, v_ in r_.items() if k_ not in ("moves",)}, flush=True)
print("FIN", _finish(nm, "park_scooter_hang (Fable's one call) from (-2.0,1.0) facing south", spot=(-2.20, 0.0)) if r_.get("status") == "done" else False, flush=True)
