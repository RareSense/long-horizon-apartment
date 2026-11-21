mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = tuple(b_ for b_ in INFO["bodies"] if b_ == pb_ or b_ == bk_ or inside(b_, bk_)); MON["ignore"] = {m.body(pb_).id}
try:
    S["dz_goal"] = S["dz"]; op.run(0.4, [cmd])
    PRE_ACTION("two_hand_release", {}); TWO["vise"] = False; two_hand_open((0.03, 0.03)); op.run(1.0, [_zero("left"), _zero("right")])
    print("released: pouch", np.round(centre(pb_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(pb_)], "inside", inside(pb_, bk_), flush=True)
    PRE_ACTION("two_hand_stand", {})
    h0_ = -0.40
    for h_ in np.linspace(h0_, 0.0, 4)[1:]:
        T = 2.5; vz = 1.24 * float(h_ - h0_) / T
        op.send(dict(cmd="posture", height=float(h_), lean=0.0, duration=T))
        op.run(T, [dict(cmd="ee", name=s_, mode="velocity", linear=[0, 0, vz], frame="world", ttl=0.3) for s_ in SIDES])
        op.run(0.6, [_zero("left"), _zero("right")]); h0_ = float(h_)
    for _ in range(2):
        tmove(fwd=-0.15, carry=("left", "right"), tag="pouch_back_off")
    hand_down("left"); hand_down("right")
    open_jaws("left", T=0.3); open_jaws("right", T=0.3); rest_hands(SIDES); stand_up(T=1.6); op.run(1.0)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print("pouch", np.round(centre(pb_), 3).tolist(), "inside", inside(pb_, bk_), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), "state", state(), "fell", fallen(), "ee", {k_: v_.get("mode") for k_, v_ in ts.ee.items()}, "touch", contact_report()["body"], flush=True)
print(close(os.path.join(TELE_DIR, "pouch_in2.jpg"), np.array([-4.9, -1.0, 1.3]), np.array([-5.18, -1.40, 0.05]), "pouch in basket"), flush=True)
