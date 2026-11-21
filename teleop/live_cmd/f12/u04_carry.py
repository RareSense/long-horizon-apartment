# Carry the umbrella (held level at pad height 0.62 by both corner pinches) west along y -1.27, then NW to the wall spot.
# Slow (0.10 m/s) with the monitor on; the slab's swept area checked by the neighbour monitor (1.2 m).
WAYS = [(2.40, -1.27, np.pi), (1.20, -1.27, np.pi), (0.40, -1.20, np.pi), (-0.60, -0.20, 2.36), (-1.78, 0.59, np.pi / 2)]
o_ = dict(legs=[])
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,); MON["held"] = {}
try:
    for wp_ in WAYS[: int(globals().get("N_LEGS", len(WAYS)))]:
        PRE_ACTION("umb_carry_leg", dict(goal=[round(wp_[0], 2), round(wp_[1], 2), round(float(np.degrees(wp_[2])))]))
        w_ = with_tight(lambda: walk_path(wp_, carry=SIDES, ignore=(UMB,), tol=0.04, v=0.10), rb=0.24, rf=(0.18, 0.10), rb0=0.22, rf0=0.12)
        rec_ = dict(goal=wp_[:2], at=np.round(base()[0][:2], 3).tolist(), yaw=round(float(np.degrees(base()[1])), 1),
                    umb=np.round(centre(UMB), 3).tolist(), hold_err={s_: round(HOLD.items[s_]["err"], 4) for s_ in SIDES if s_ in HOLD.items},
                    lost={s_: hold_lost(s_) for s_ in SIDES}, touch=[c_ for c_ in umb_contacts() if ":" not in c_[0]])
        o_["legs"].append(rec_)
        print("LEG", rec_, flush=True)
        if any(rec_["lost"].values()):
            raise Abort("hold lost")
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
MON["on"] = False
o_.update(state=state(), fell=fallen())
print("U04", {k_: v_ for k_, v_ in o_.items() if k_ != "legs"}, flush=True)
print(look3("f12_u04_carry"), flush=True)
