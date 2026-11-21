def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
def zz_dump():
    c_ = ts.ctrl; o_ = {}
    for k_ in ("q_post", "com_goal", "com_shift", "ext", "_payload", "effort_bias", "_w_override", "com_axes", "point_support", "line_support", "yield_dirs", "load_aware", "arm_qd_on", "f_max"):
        v_ = getattr(c_, k_, None)
        o_[k_] = (np.round(v_, 3).tolist() if isinstance(v_, np.ndarray) else str(v_)[:300])
    return o_
zz_D = {}
for nm_, ck_ in (("good0182", r"C:\Users\raresense\sim_home\runs\1120_072140_dex1_floor_9\checkpoints\0182_item_r125i1_flat"), ("bad0408", r"C:\Users\raresense\sim_home\runs\1120_075248_dex1_floor_10\checkpoints\0408_item_r178i1_ball")):
    ck_load(ck_); gait_on(); settle_after_load(); refresh_jointed_footprints()
    op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
    zz_D[nm_] = zz_dump()
    print(nm_, "tilt at H_WALK", zz_tl(), state()["pelvis"], flush=True)
for k_ in zz_D["good0182"]:
    if zz_D["good0182"][k_] != zz_D["bad0408"][k_]:
        print("DIFF", k_, "\n  good", str(zz_D["good0182"][k_])[:400], "\n  bad ", str(zz_D["bad0408"][k_])[:400], flush=True)
print("lean", ts.lean, "loco g diff check", {k_: v_ for k_, v_ in ts.loco.g.items() if not isinstance(v_, (list, dict))}, flush=True)
