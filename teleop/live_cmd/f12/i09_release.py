MON["on"] = False
PRE_ACTION("open_jaws_over_bin", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}
op.run(1.0)
print("pouch", np.round(centre(zz_b), 3).tolist(), "in bin", inside(zz_b, binb_), flush=True)
mon_start(target=None)
try:
    hp_ = ts.ee_pose(SD)[0]
    op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.15, timeout=2.0, tol=0.02)
    p_, y_ = base()
    tg_ = np.r_[p_[:2] + RM.rz(y_)[:2, :2] @ np.array([0.05, 0.30]), 0.75]
    op.move({SD: tg_.tolist()}, speed=0.15, timeout=3.0, tol=0.03)
    rest_hands(SIDES, T=0.8)
    tmove(fwd=-0.12, tag="off_bin")
except Abort as ex_:
    print("ABORT", str(ex_)[:200], flush=True)
MON["on"] = False
print("pouch", np.round(centre(zz_b), 3).tolist(), "in bin", inside(zz_b, binb_), "bin", np.round(centre(binb_), 3).tolist(), "state", state(), "touch", contact_report()["body"], flush=True)
if inside(zz_b, binb_):
    print("DONE", item_done_auto("r149i1_pouch", dict(status="done", how="AI teleop after the library surface pick missed twice (corner of a 9.5 x 15 x 3 cm 50 g pouch: it pivoted, rose 2.4 cm < 4 cm check) and a pinch without hold slipped at 2.5 cm: corner pinch 1.8 cm in at the corner nearest the robot, contact check (both fingers on side faces), hold_on, lifted 19 cm; put_away to the bin stopped on the knee at the bin (31 N) with the pouch already over the opening: dropped in (AI-operated)")), flush=True)
print(look3("f12_pouch_in_bin"), flush=True)
