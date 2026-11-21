MON["on"] = False
PRE_ACTION("open_jaws", {}); open_jaws(SD, T=0.5); HELD.pop(SD, None); MON["held"] = {}; op.run(0.5)
hp_ = pad_mid(SD); servo_pads(SD, hp_[:2], hp_[2] + 0.15, QB, speed=0.08, n=1)
crouch(-0.20, 0.35, T=1.2); crouch(0.0, 0.0, T=1.2); rest_hands(SIDES, T=0.6)
print("released", np.round(centre(zz_b), 3).tolist(), state(), flush=True)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\basket_put.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\qc_patch.py", encoding="utf-8").read())
T3 = toy_trip("r193i1_toy_piece", note=" (re-pick with the right hand after a left-hand put failed)")
