zz_cks = sorted(_gl.glob(r"C:\Users\raresense\sim_home\runs\1119_220839_dex1_floor_4\checkpoints\*_act_tele_move"))
ck_load(zz_cks[-1]); print("loaded", zz_cks[-1], state())
SC_NAME = "r126i1_scooter"; zz_b = body_of(SC_NAME)
mon_start(target=zz_b); MON["ignore_names"] = (body_of("r130i1_light_saber"),); MON["held"] = {s_: zz_b for s_ in SIDES}
TELE_V = V_CARRY_HEAVY; TELE_W = 0.10; CARRY_LOW = False
MON["trace"] = []
for zz_k in range(2):
    try:
        zz_r = _sc_mv("sc_probe_turn", turn=5.0)
        print("turn5", zz_r, flush=True)
    except Abort as ex:
        print("ABORT", ex, state(), _sc_in_jaws(zz_b)); break
print("trace", MON["trace"][::3])
MON["trace"] = None; MON["on"] = False
TELE_W = 0.15
