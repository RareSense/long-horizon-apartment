# Sponges retry 1 (AI-operated) from the act checkpoint before the last walk leg (0446_act_walk, robot at (0.558,0.066)
# facing east). SEEN at the stop: at walk height (pelvis z 0.673) the knees are 0.19 m ahead of the pelvis; at the
# stance x 0.708 the right knee shell touched the island's base face (contact x 0.96, z 0.26, 65 N) in the settling
# swing. Fix: stance 2.8 cm further back (x 0.68): knee front ~0.93, 3 cm off the face. Everything else Fable's call.
CK_ = os.path.join(RUN, "checkpoints", "0446_act_walk")
route_v3_resume(CK_)
print(gait_on())
settle_after_load()
refresh_jointed_footprints()
rest_hands(SIDES); op.run(1.0)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync_cloth", str(ex_)[:100])
print("loaded", CK_, state(), "kit", kit_mem(), flush=True)
SP_STAND = (0.68, 0.066, 0.0)
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f14\c01_sponges.py", encoding="utf-8").read())
