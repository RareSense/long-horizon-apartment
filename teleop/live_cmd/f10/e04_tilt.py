import json as _js
ck_load(os.path.join(RUN, "checkpoints", "0186_item_r175i1_cardboard_box")); gait_on(); settle_after_load(); refresh_jointed_footprints()
def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
print("stand", state()["pelvis"], "pelvis tilt", zz_tl(), "H_WALK", H_WALK, flush=True)
op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
print("waist", [(m.joint(j_).name, round(float(d.qpos[m.jnt_qposadr[j_]]), 3)) for j_ in range(m.njnt) if "waist" in m.joint(j_).name], flush=True)
