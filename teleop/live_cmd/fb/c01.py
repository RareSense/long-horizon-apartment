ck_load(os.path.join(RUN, "checkpoints", "0208_act_fb_E_low_in_hamper_before_release"))
gait_on(); settle_after_load()
print("loaded", "pad", np.round(pad_mid("right"), 3).tolist(), "held", cloth_held("right"), "LOCK", {s_: len(v_[1]) for s_, v_ in LOCK.items()}, "blanket", in_container(zz_BL, zz_hb()), "pelvis", state()["pelvis"], "tilt", round(pelvis_tilt(), 3), "hamper", np.round(obj_rect(zz_hb()).c, 3).tolist(), flush=True)
# the held end back up over the centre: the strand from the rim to the hand becomes taut
ZZ_TARGETS = [(0.60, -0.05, 0.95), (0.62, -0.05, 1.10), (0.62, -0.05, 1.18)]
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\b20.py", encoding="utf-8").read())
