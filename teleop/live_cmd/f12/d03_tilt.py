def R_tilt(cd, u, deg):
    """R_down(cd) turned about the closing direction so the finger tips trail the push by deg (the jaw tips are a
    pencil point: pushed upright the slab edge meets the taper and lifts the hand over it, seen run 1120_093820)."""
    R0_ = R_down(cd); cd3_ = np.r_[cd, 0.0] / np.linalg.norm(cd)
    k_ = int(np.argmin([R0_[:, j_] @ np.array([0, 0, 1.0]) for j_ in range(3)]))   # the column pointing down = finger axis
    best_ = None
    for sg_ in (1.0, -1.0):
        a_ = np.radians(deg) * sg_
        K_ = np.array([[0, -cd3_[2], cd3_[1]], [cd3_[2], 0, -cd3_[0]], [-cd3_[1], cd3_[0], 0]])
        Rr_ = np.eye(3) + np.sin(a_) * K_ + (1 - np.cos(a_)) * K_ @ K_
        R_ = Rr_ @ R0_
        if best_ is None or R_[:2, k_] @ u < best_[1][:2, k_] @ u:
            best_ = (sg_, R_)
    return best_[1]


SIDE = "left"; U = np.array([-1.0, 0.0]); CD = np.array([-U[1], U[0]])
TILT = 18.0
QT = {SIDE: q_(R_tilt(CD, U, TILT))}
mon_start(target=None); MON["ignore"] = {m.body(UMB).id}; MON["ignore_names"] = (UMB,)
log_ = []
try:
    e_, _t = slab_entry(np.array([3.0, -1.20]), U)
    pm_ = pad_mid(SIDE)
    PRE_ACTION("hand_tilt", {}); servo_pads(SIDE, e_ - U * 0.04, 0.06, QT, speed=0.05, n=2)
    print("e", np.round(servo_pads(SIDE, e_ - U * 0.03, 0.018, QT, speed=0.04, n=3), 3).tolist(), "pad", np.round(pad_mid(SIDE), 3).tolist(), flush=True)
    for k_ in range(4):
        c0_ = centre(UMB)[:2].copy()
        PRE_ACTION("push", dict(k=k_)); servo_pads(SIDE, pad_mid(SIDE)[:2] + U * 0.03, 0.018, QT, speed=0.04, n=3)
        log_.append((k_, round(float((centre(UMB)[:2] - c0_) @ U), 3), np.round(pad_mid(SIDE), 3).tolist(), round(ahead_of_pelvis(pad_mid(SIDE)), 3)))
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
print("log", log_, flush=True)
pm_ = pad_mid(SIDE)
print("state", state(), "umb", np.round(centre(UMB), 3).tolist(), flush=True)
print(close(os.path.join(TELE_DIR, "f12_d03_side.jpg"), np.r_[pm_[:2] + np.array([0.0, -0.45]), 0.12], np.r_[pm_[:2], 0.02], "tilt push side"), flush=True)
