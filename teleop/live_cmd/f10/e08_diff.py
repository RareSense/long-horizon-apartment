def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
def zz_flat(o_, pre_, out_, depth=0):
    for k_, v_ in list(vars(o_).items()):
        if k_.startswith("__"): continue
        if isinstance(v_, (int, float, bool, str)) or v_ is None:
            out_[pre_ + k_] = v_
        elif isinstance(v_, np.ndarray) and v_.size <= 40:
            out_[pre_ + k_] = np.round(np.asarray(v_, float), 3).tolist() if v_.dtype != bool else v_.tolist()
        elif isinstance(v_, dict) and len(v_) < 80:
            out_[pre_ + k_] = str({kk_: (np.round(np.asarray(vv_, float), 3).tolist() if isinstance(vv_, np.ndarray) else vv_) for kk_, vv_ in v_.items()})[:400]
    return out_
zz_D = {}
for nm_, ck_ in (("good", r"C:\Users\raresense\sim_home\runs\1120_072140_dex1_floor_9\checkpoints\0182_item_r125i1_flat"), ("bad", r"C:\Users\raresense\sim_home\runs\1120_075248_dex1_floor_10\checkpoints\0408_item_r178i1_ball")):
    ck_load(ck_); gait_on(); settle_after_load()
    op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
    o_ = {}
    zz_flat(ts, "ts.", o_); zz_flat(ts.loco, "loco.", o_); zz_flat(ts.ctrl, "ctrl.", o_)
    zz_D[nm_] = o_; print(nm_, zz_tl(), flush=True)
skip_ = ("pos", "com", "anc", "xi", "t0", "time", "yaw", "foot", "sole", "p_", "base")
for k_ in zz_D["good"]:
    if k_ in zz_D["bad"] and zz_D["good"][k_] != zz_D["bad"][k_] and not any(s_ in k_.lower() for s_ in skip_):
        print("DIFF", k_, "| good", str(zz_D["good"][k_])[:200], "| bad", str(zz_D["bad"][k_])[:200], flush=True)
