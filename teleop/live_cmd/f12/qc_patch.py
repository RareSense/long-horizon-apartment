# Session patch (20 Nov grasp QC, AI-operated): skills.py hold_guard / close_jaws without re-exec of skills.py.
CLOSE_REF = {}                                   # side -> (time closed, xpos / xmat before the close, xpos / xmat after it)
HOLD_REFUSED = []


def jaw_fingers_on(s, name):
    """The jaw finger links of hand s that touch body `name` now (simulated contacts, br.mjd)."""
    if not (hasattr(br, "mjd") and hasattr(br, "sb_of_ib")):
        return set()
    md = br.mjd; sb = br.sb_of_ib; gb = br.geom_body; bb = m.body(name).id; fs = set(FINGER[s]); out = set()
    for i in range(int(md.ncon)):
        c = md.contact[i]
        b0, b1 = int(sb[gb[int(c.geom[0])]]), int(sb[gb[int(c.geom[1])]])
        if b0 == bb and b1 in fs:
            out.add(b1)
        elif b1 == bb and b0 in fs:
            out.add(b0)
    return out


def hold_guard(s, name):
    """Grasp QC before the contact-verified hold (20 Nov, user's video QC: plastic bag r196 was welded after one jaw tip
    had flipped it onto its edge during the close; grip_check(side, None) looks at no object). Refused unless BOTH jaw
    fingers of hand s touch this thing, and, when the close was recorded (CLOSE_REF), the thing rose < 5 mm and turned
    < 10 deg while the jaws closed. -> (ok, why)."""
    f_ = jaw_fingers_on(s, name)
    if len(f_) < 2:
        return False, f"{len(f_)} jaw finger(s) on {name}"
    ref = CLOSE_REF.get(s)
    if ref is not None and float(d.time) - ref[0] < 30.0:
        b = m.body(name).id
        dz = float(ref[3][b][2] - ref[1][b][2])
        Rr = ref[2][b].reshape(3, 3); Rn = ref[4][b].reshape(3, 3)
        ang = float(np.degrees(np.arccos(np.clip((np.trace(Rr.T @ Rn) - 1.0) / 2.0, -1.0, 1.0))))
        if dz > 0.005 or ang > 10.0:
            return False, f"{name} moved in the close: rose {dz * 1000:.1f} mm, turned {ang:.1f} deg"
    return True, ""



if "_hold_on_noguard" not in globals():
    _hold_on_noguard = hold_on


def hold_on(s, name, share=1.0, guard=True):
    if guard and HOLD is not None and HOLD_USE:
        ok_, why_ = hold_guard(s, name)
        if not ok_:
            HOLD_REFUSED.append(dict(t=round(float(d.time), 2), side=s, obj=name, why=why_))
            EVENTS.append(dict(t=round(float(d.time), 2), ev="hold REFUSED (grasp QC)", obj=name, side=s, why=why_))
            print(f"[hold] REFUSED {s} on {name}: {why_}", flush=True)
            return False
    return _hold_on_noguard(s, name, share)


def close_jaws(s, force=12.0, T=0.8):
    x0_, R0_ = d.xpos.copy(), d.xmat.copy()                          # hold_guard: did the thing rise / turn IN the close
    jaw_force[s] = float(force); jaw_target[s] = 0.0; op.run(T)
    CLOSE_REF[s] = (float(d.time), x0_, R0_, d.xpos.copy(), d.xmat.copy())


print("[grasp QC] hold_guard on hold_on, close_jaws records the close", flush=True)
