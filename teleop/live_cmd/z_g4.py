zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece")
TUCK_JOINTS = False
STANCE_LOW_ROOM = 0.35
STANCE_FUR_ROOM = 0.32
floor_first(["r131i1_knit_hat", "r189i1_santa_hat", "r121i1_jacket", "r117i1_blanket", "r116i1_coat_pile", "r190i1_stocking", "r68i1_rag"])
# out of the pocket to the east (AI-operated) in short re-aimed steps (step_wp: turn <= 15 deg, step <= 0.12 m, stand,
# re-aim): the walk legs drifted 0.3 m to the left on a 0.4 m diagonal leg (trace t 870-878) and the left gripper knocked
# the scooter 5.8 cm; the planner's way and a 90 deg turn on the spot failed before (scooter stem, ball r192)
mon_start()
zz_ok = True; zz_log = []
try:
    for zz_wp, zz_tol in [((-2.32, -1.24), 0.07), ((-1.45, -1.18), 0.10)]:
        for _k in range(16):
            tr_, ds_ = aim(zz_wp)
            if ds_ < zz_tol:
                break
            r_ = step_wp(zz_wp, "tx", fwd_max=0.12)
            zz_log.append((r_[0], r_[1], r_[2]["at"], r_[2]["yaw_deg"]))
            if MON.get("why"):
                raise Abort(MON["why"])
        print("at", zz_wp, state(), flush=True)
except Abort as ex:
    zz_ok = False; print("TRANSIT ABORT", ex)
MON["on"] = False
print("transit", zz_ok, state(), "steps", zz_log)
print(look3("transit_east"), kit_mem())
if zz_ok:
    zz_ck_tr = ck_save("transit_east_ok", kind="act")
    print("ckpt", zz_ck_tr)
    zz_gr = go_item()
