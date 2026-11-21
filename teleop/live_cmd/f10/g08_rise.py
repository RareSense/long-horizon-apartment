exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
bk_ = body_of("r186i1_basket"); h = op._hold
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = tuple(b_ for b_ in INFO["bodies"] if b_ == pb_ or b_ == bk_ or inside(b_, bk_)); MON["ignore"] = {m.body(pb_).id}
try:
    S = dict(cz0=float(h["c_ref"][2]), pz0=float(base()[0][2]), dz=0.0, dz_goal=0.0)
    xy0_ = centre(pb_)[:2].copy()
    cmd = lambda: _two_track(pb_, xy0_, S)
    PRE_ACTION("two_hand_rise", {})
    for hh_ in (-0.30, -0.15, 0.0):
        op.send(dict(cmd="posture", height=hh_, lean=0.0, duration=2.5)); op.run(3.0, [cmd])
        print("rise", hh_, "pelvis", state()["pelvis"], "pouch", np.round(centre(pb_), 3).tolist(), {s_: zz_force(s_) for s_ in SIDES}, flush=True)
    TWO["vise"] = False; two_seat(); two_keep(1.0)
    r_ = tmove(fwd=0.08, carry=SIDES, tag="pouch_closer2")
    print("closer", r_["at"], r_["yaw_deg"], r_["touch"]["body"], "pouch", np.round(centre(pb_), 3).tolist(), {s_: zz_force(s_) for s_ in SIDES}, flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
