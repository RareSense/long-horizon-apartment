CK_RELOAD = os.path.join(CK_DIR, "0666_act__turn_on_spot")
ck_load(CK_RELOAD); gait_on(); op.run(0.3)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync", ex_)
print("RELOADED", CK_RELOAD, "frame", rec.n, state(), flush=True)
def _d5():
    g = room_grid(("r117i1_blanket",))
    for s_ in ((-2.2, -1.13), (-2.0, -1.13), (-1.8, -1.15), (-1.6, -1.15), (-1.4, -1.15), (-1.2, -1.2), (-1.0, -1.2), (-1.4, -1.3), (-1.2, -1.0)):
        print("start", s_, "cost", round(float(g.reach_cost(np.array(s_), np.array([0.91, -1.5]))), 2), flush=True)
with_tight(_d5)
for b_ in INFO["bodies"]:
    try:
        c_ = centre(b_)
    except Exception:
        continue
    if -2.6 < c_[0] < -0.8 and -1.8 < c_[1] < -0.9:
        print("thing", b_, INFO["bodies"][b_].get("display"), np.round(c_, 2).tolist(), [np.round(v_, 2).tolist() for v_ in obj_box(b_)], flush=True)
