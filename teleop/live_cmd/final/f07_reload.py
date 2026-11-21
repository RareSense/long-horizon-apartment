CK_RELOAD = os.path.join(CK_DIR, "0666_act__turn_on_spot")
ck_load(CK_RELOAD); gait_on(); op.run(0.3)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync", ex_)
print("RELOADED", CK_RELOAD, "frame", rec.n, state(), flush=True)
sc_ = body_of("r126i1_scooter")
print("scooter box", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], "centre", np.round(centre(sc_), 3).tolist(), flush=True)
try:
    print("scooter hull", np.round(flat_corners(sc_)[0], 3).tolist(), flush=True)
except Exception as ex_:
    print("hull ERR", ex_)
print("near", near_things(1.0), flush=True)
def _d3():
    g = room_grid(("r117i1_blanket",))
    for s_ in ((-2.4, -0.95), (-2.4, -0.8), (-2.3, -0.7), (-2.2, -0.6), (-2.11, -0.52), (-2.0, -0.45), (-1.9, -0.4), (-1.6, -0.35), (-1.3, -0.5)):
        print("start", s_, "cost", round(float(g.reach_cost(np.array(s_), np.array([0.91, -1.5]))), 2), flush=True)
with_tight(_d3)
print(look3("f07_reloaded"), flush=True)
