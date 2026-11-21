MON["on"] = False
CHAIN = r"C:/Users/raresense/sim_home/runs/1120_084921_dex1_floor_11/checkpoints/0373_item_r179i1_toy_pouch"
zz_m = route_v3_resume(CHAIN)
print(gait_on(), flush=True)
settle_after_load()
refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 6]], "done", len(DONE), "state", state(), flush=True)
sb_ = body_of("r126i1_scooter")
print("scooter box", [np.round(v_, 3).tolist() for v_ in obj_box(sb_)], flush=True)
loose_ = []
for b_ in INFO["bodies"]:
    try: lo_, hi_ = obj_box(b_)
    except Exception: continue
    c_ = (lo_ + hi_) / 2
    if b_ != sb_ and lo_[2] < 0.25 and -2.4 < c_[0] < -1.2 and -1.1 < c_[1] < 0.9:
        loose_.append((b_, INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist()))
print("loose in x -2.4..-1.2 y -1.1..0.9:", loose_, flush=True)
mon_start(target=None)
try:
    w_ = walk_tight((-2.0, 1.0, -1.47))
    print("walk", {k_: v_ for k_, v_ in (w_ or {}).items() if k_ in ("ok", "err_xy", "err_yaw")} if isinstance(w_, dict) else str(w_)[:300], flush=True)
except Abort as ex_:
    print("ABORT walk", str(ex_)[:300], flush=True)
MON["on"] = False
print("state", state(), "fell", fallen(), flush=True)
print(look3("f12_scooter_start"), flush=True)
