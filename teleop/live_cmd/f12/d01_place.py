SIDE = "left"; U = np.array([-1.0, 0.0]); CD = np.array([-U[1], U[0]]); QL = {SIDE: q_(R_down(CD))}
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
try:
    tmove(fwd=0.05, tag="f12_closer")
    print("after move", state()["pelvis"], flush=True)
    PRE_ACTION("close_jaws", dict(side=SIDE)); close_jaws(SIDE, 10.0, T=0.6)
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8), (-0.40, 0.85)):
        PRE_ACTION("squat", dict(h=hh_, l=ll_)); crouch(hh_, ll_, T=1.2)
    e_, _t = slab_entry(np.array([3.0, -1.20]), U)
    p0_ = e_ - U * 0.03
    print("edge", np.round(e_, 3).tolist(), "p0 ahead", round(ahead_of_pelvis(p0_), 3), flush=True)
    PRE_ACTION("hand_above", {}); servo_pads(SIDE, p0_, 0.20, QL, speed=0.10, n=2)
    PRE_ACTION("hand_down", {}); print("e_down", np.round(servo_pads(SIDE, p0_, 0.022, QL, speed=0.05, n=3), 3).tolist(), flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
pm_ = pad_mid(SIDE)
print("pad", np.round(pm_, 3).tolist(), "state", state(), "touch", contact_report()["body"], flush=True)
# finger geometry z min of the left hand links
lo_z = min(float(d.xpos[m.body(n_).id][2]) for n_ in [m.body(i_).name for i_ in range(m.nbody)] if n_.startswith("left_") and ("finger" in n_ or "jaw" in n_ or "hand" in n_ or "gripper" in n_)) if True else None
print("lowest left hand body z", round(lo_z, 3), flush=True)
print(close(os.path.join(TELE_DIR, "f12_d01_side.jpg"), np.r_[pm_[:2] + np.array([0.0, -0.45]), 0.12], np.r_[pm_[:2], 0.02], "pad side"), flush=True)
