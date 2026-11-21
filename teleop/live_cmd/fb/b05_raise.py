exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\zz_arm.py", encoding="utf-8").read())
PRE_ACTION("zz_stand_full", {})
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=1.0)); op.run(1.6)
print("stood", state()["pelvis"], "pad_rf", np.round(zz_to_rf(pad_mid(zz_sd)), 3).tolist(), flush=True)
for zz_t in ZZ_TARGETS:
    zz_r = zz_pads_to(zz_sd, zz_rf(zz_t), Q=None, speed=0.12)
    print("to", zz_t, zz_r, "hang", zz_hang(zz_sd), "lowest", round(float(zz_w().points(0)[:, 2].min()), 3), "fell", fallen(), contact_report(), flush=True)
op.run(1.5)
zz_P = zz_w().points(0)
print("C world", np.round(zz_P[994], 3).tolist(), "C rf", np.round(zz_to_rf(zz_P[994]), 3).tolist(), "pad", np.round(pad_mid(zz_sd), 3).tolist(), "hang", zz_hang(zz_sd), flush=True)
for zz_z in (1.0, 0.9, 0.8, 0.7, 0.6, 0.4, 0.2):
    print("bunch z", zz_z, zz_bunch(zz_z), flush=True)
print("look", zz_look(pad_mid(zz_sd) - np.array([0, 0, 0.45]), "E_raised", dist=1.6, h=0.3, dirs=(120.0, 210.0, 300.0, 30.0)), flush=True)
