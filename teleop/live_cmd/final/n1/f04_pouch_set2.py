rec.still_every = 300
pb_ = body_of("r179i1_toy_pouch"); bk_ = body_of("r186i1_basket"); h = op._hold; xy_ = np.array([-5.10, -1.36])
ck_load(os.path.join(RUN, "checkpoints", [c_ for c_ in sorted(os.listdir(os.path.join(RUN, "checkpoints"))) if c_.endswith("_act_n1_pouch_at_basket")][-1])); gait_on()
TWO["on"] = True; TWO["vise"] = False; two_keep(4.0); two_keep(1.5)
print("RELOADED pouch_at_basket rec", rec.n, "F", {s_: zz_force(s_, pb_) for s_ in SIDES}, "pouch", np.round(centre(pb_), 3).tolist(), flush=True)
def zz_touch():
    return [c_ for c_ in _thing_contacts(pb_) if "Dex1" not in c_ and "wrist" not in c_]
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = tuple(b_ for b_ in INFO["bodies"] if b_ == pb_ or b_ == bk_ or inside(b_, bk_)); MON["ignore"] = {m.body(pb_).id}
zz_st = []
try:
    two_reanchor(ride=False); TWO["vise"] = True; two_keep(0.5)
    S = dict(cz0=float(h["c_ref"][2]), pz0=float(base()[0][2]), dz=0.0, dz_goal=0.0)
    cmd = lambda: _two_track(pb_, xy_, S)
    op.run(4.0, [cmd])
    for hh_, ll_ in ((-0.05, 0.3), (-0.12, 0.5), (-0.20, 0.6), (-0.28, 0.7), (-0.34, 0.8)):
        PRE_ACTION("two_hand_squat", dict(h=hh_, l=ll_)); op.send(dict(cmd="posture", height=hh_, lean=ll_, duration=2.5)); op.run(3.5, [cmd])
        zz_st.append((hh_, ll_, round(float(obj_box(pb_)[0][2]), 3), np.round(xy_ - centre(pb_)[:2], 3).tolist(), {s_: zz_force(s_, pb_) for s_ in SIDES}, zz_touch()))
        print("stage", zz_st[-1], flush=True)
        if zz_touch(): break
    PRE_ACTION("two_hand_lower", {})
    S["dz_goal"] = S["dz"] - 0.15
    for k_ in range(44):
        op.run(0.25, [cmd])
        if zz_touch(): break
    print("arms: bottom", round(float(obj_box(pb_)[0][2]), 3), "err", np.round(xy_ - centre(pb_)[:2], 3).tolist(), "touch", zz_touch(), {s_: zz_force(s_, pb_) for s_ in SIDES}, flush=True)
    S["dz_goal"] = S["dz"]; op.run(0.4, [cmd])
    PRE_ACTION("two_hand_release", {}); TWO["vise"] = False; two_hand_open((0.03, 0.03)); op.run(1.0, [_zero("left"), _zero("right")])
    TWO["on"] = False; HELD.pop("left", None); HELD.pop("right", None)
    print("released: pouch", np.round(centre(pb_), 3).tolist(), "inside", inside(pb_, bk_), flush=True)
    PRE_ACTION("two_hand_stand", {})
    for hh_, ll_ in ((-0.30, 0.6), (-0.24, 0.45), (-0.16, 0.3), (-0.08, 0.15), (0.0, 0.0)):
        op.send(dict(cmd="posture", height=hh_, lean=ll_, duration=1.8))
        op.run(1.8, [dict(cmd="ee", name=s_, mode="velocity", linear=[0, 0, 0.06], frame="world", ttl=0.3) for s_ in SIDES])
        op.run(0.5, [_zero("left"), _zero("right")])
        print("up", hh_, state()["pelvis"], "fell", fallen(), flush=True)
    for _ in range(2):
        tmove(fwd=-0.15, carry=("left", "right"), tag="pouch_back_off")
    hand_down("left"); hand_down("right")
    open_jaws("left", T=0.3); open_jaws("right", T=0.3); rest_hands(SIDES); stand_up(T=1.6); op.run(1.0)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("pouch", np.round(centre(pb_), 3).tolist(), "inside", inside(pb_, bk_), "check", item_check("r179i1_toy_pouch"), "state", state(), "fell", fallen(), "ee", {k_: v_.get("mode") for k_, v_ in ts.ee.items()}, "touch", contact_report()["body_who"], flush=True)
print(look3("n1_pouch_in"), flush=True)
