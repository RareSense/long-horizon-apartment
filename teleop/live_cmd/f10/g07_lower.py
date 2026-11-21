exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
bk_ = body_of("r186i1_basket"); xy_ = np.array([-5.10, -1.36]); h = op._hold
def zz_touch():
    return [c_ for c_ in _thing_contacts(pb_) if "Dex1" not in c_ and "wrist" not in c_]
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = tuple(b_ for b_ in INFO["bodies"] if b_ == pb_ or b_ == bk_ or inside(b_, bk_)); MON["ignore"] = {m.body(pb_).id}
zz_out = dict(stages=[])
try:
    PRE_ACTION("two_hand_vise", {})
    TWO["vise"] = False; two_seat(); two_keep(1.0); two_reanchor(ride=False); TWO["vise"] = True; two_keep(1.0)
    S = dict(cz0=float(h["c_ref"][2]), pz0=float(base()[0][2]), dz=0.0, dz_goal=0.0)
    cmd = lambda: _two_track(pb_, xy_, S)
    PRE_ACTION("two_hand_servo", {}); op.run(6.0, [cmd])
    zz_out["standing_err"] = np.round(xy_ - centre(pb_)[:2], 3).tolist()
    hn_ = 0.0
    while hn_ > -0.40 and not zz_touch() and float(obj_box(pb_)[0][2]) > 0.16:
        hn_ -= 0.05
        PRE_ACTION("two_hand_squat", dict(h=hn_)); op.send(dict(cmd="posture", height=hn_, lean=0.0, duration=2.5)); op.run(3.0, [cmd])
        zz_out["stages"].append((round(hn_, 2), round(float(obj_box(pb_)[0][2]), 3), np.round(xy_ - centre(pb_)[:2], 3).tolist(), {s_: zz_force(s_) for s_ in SIDES}, zz_touch()))
        print("stage", zz_out["stages"][-1], flush=True)
    if not zz_touch():
        PRE_ACTION("two_hand_lean", {}); op.send(dict(cmd="posture", height=hn_, lean=globals().get("ZZ_LEAN", 0.2), duration=2.5)); op.run(3.0, [cmd])
        S["dz_goal"] = -0.06; op.run(4.5, [cmd])
    zz_out.update(bottom=round(float(obj_box(pb_)[0][2]), 3), err=np.round(xy_ - centre(pb_)[:2], 3).tolist(), touch=zz_touch(), h=hn_)
    print("low", zz_out, flush=True)
except Abort as ex_:
    zz_out["abort"] = str(ex_)
MON["on"] = False
print("OUT", str(zz_out)[:600], "state", state(), "fell", fallen(), flush=True)
print(look3("pouch_low"), flush=True)
