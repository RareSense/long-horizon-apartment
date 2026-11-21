exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f12\slab.py", encoding="utf-8").read())
e_, _t = slab_entry(np.array([3.0, -1.20]), np.array([-1.0, 0.0]))
gap_ = ahead_of_pelvis(e_)
print("edge ahead of pelvis", round(gap_, 3), flush=True)
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}
try:
    if gap_ > 0.29:
        tmove(fwd=float(gap_ - 0.27), tag="f12_to_edge")
except Abort as ex_:
    print("ABORT move", str(ex_)[:300], flush=True)
MON["on"] = False
print("state", state(), "edge ahead", round(ahead_of_pelvis(e_), 3), flush=True)
r_ = slab_push("left", (-1.0, 0.0), (3.0, -1.20))
print("PUSH", r_, flush=True)
print(close(os.path.join(TELE_DIR, "f12_push2_top.jpg"), np.array([2.6, -0.9, 2.2]), np.array([2.3, -1.2, 0.0]), "push2 top"), flush=True)
