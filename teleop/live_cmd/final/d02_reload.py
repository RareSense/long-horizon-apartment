ball_ = body_of("r192i1_ball")
print("ball now", np.round(centre(ball_), 3).tolist(), flush=True)
CK_RELOAD = os.path.join(CK_DIR, "0342_act_put_down")
zz_m = ck_load(CK_RELOAD)
gait_on(); op.run(0.3)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync", ex_)
print("RELOADED", CK_RELOAD, "frame", rec.n, "state", state(), "held", {s_: HOLD.holding(s_) for s_ in SIDES}, flush=True)
print("ball", np.round(centre(ball_), 3).tolist(), "toy", np.round(centre(body_of("r193i3_toy_piece")), 3).tolist(), "r193i1", np.round(centre(body_of("r193i1_toy_piece")), 3).tolist(), flush=True)
print("near", near_things(0.9), flush=True)
print(look3("d02_reload"), flush=True)
