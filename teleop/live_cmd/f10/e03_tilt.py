import json as _js
ck_load(os.path.join(RUN, "checkpoints", "0408_item_r178i1_ball")); gait_on(); settle_after_load(); refresh_jointed_footprints()
def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
print("stand", state()["pelvis"], "pelvis tilt", zz_tl(), "H_WALK", H_WALK, flush=True)
op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
print("at H_WALK", state()["pelvis"], "pelvis tilt", zz_tl(), "legs", np.round(d.qpos[7:19], 2).tolist(), flush=True)
for k_ in ("lean", "height", "posture", "R_up", "up_target"):
    for o_ in (ts, getattr(ts, "ctrl", None), getattr(ts, "sess", None)):
        if o_ is not None and hasattr(o_, k_):
            print(k_, type(o_).__name__, str(getattr(o_, k_))[:200], flush=True)
print([a_ for a_ in dir(ts) if "lean" in a_.lower() or "up" in a_.lower() or "post" in a_.lower()][:30], flush=True)
