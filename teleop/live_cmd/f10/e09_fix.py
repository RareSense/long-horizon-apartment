def zz_tl():
    R_ = d.xmat[m.body("pelvis").id].reshape(3, 3); return round(float(np.arccos(np.clip(R_[2, 2], -1, 1))), 3)
ck_load(r"C:\Users\raresense\sim_home\runs\1120_075248_dex1_floor_10\checkpoints\0408_item_r178i1_ball"); gait_on()
rest_hands(SIDES); settle_after_load(); refresh_jointed_footprints()
print("ee", {k_: v_.get("mode") for k_, v_ in ts.ee.items()}, "reach", list(ts.ctrl._reach.keys()), flush=True)
PRE_ACTION("posture_test", {})
op.send(dict(cmd="posture", height=H_WALK, lean=0.0, duration=1.0)); op.run(1.5)
print("H_WALK tilt", zz_tl(), state(), flush=True)
