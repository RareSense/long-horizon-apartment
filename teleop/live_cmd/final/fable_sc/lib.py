# AI-operated (Fable escalation, scooter r126): helpers for the live steps.
nm = "r126i1_scooter"; sc_ = body_of(nm); SC_NAME = nm


def arm_lim(s_):
    out_ = {}
    for j_ in range(m.njnt):
        n_ = m.joint(j_).name
        if n_.startswith(s_ + "_") and any(k_ in n_ for k_ in ("shoulder", "elbow", "wrist")):
            out_[n_.replace(s_ + "_", "").replace("_joint", "")] = round(float(d.qpos[m.jnt_qposadr[j_]]), 2)
    return out_


def diag(tag, tg_=None):
    p_, y_ = base(); F_ = sh_frame(sc_); R2_ = RM.rz(y_)[:2, :2]
    print(f"[{tag}] pelvis", np.round(p_, 3), "yaw", round(float(np.degrees(y_)), 1), "bar c", np.round(F_["c"], 3), "z", round(F_["z"], 3), "bar_rel", np.round(R2_.T @ (F_["c"] - p_[:2]), 3),
          "box", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], "why", MON.get("why"), "fallen", fallen(), flush=True)
    for s_ in SIDES:
        pm_ = pad_mid(s_); fx_ = ts.ee_pose(s_)[1][:, 0]
        e_ = (np.asarray(tg_[s_]) - pm_) if tg_ is not None else np.zeros(3)
        print(f"[{tag}] {s_} pad", np.round(pm_, 3), "err", np.round(e_, 3), "err body", np.round(R2_.T @ e_[:2], 3), "rel pelvis", np.round(R2_.T @ (pm_[:2] - p_[:2]), 3),
              "fingers", np.round(fx_, 2), "touch", finger_touch(s_, sc_), "gap", round(gap(s_), 4), "q", arm_lim(s_), flush=True)
    print(f"[{tag}] contacts", contact_report(), "rec", rec.n, flush=True)


def views(tag):
    p_, y_ = base(); fw_ = np.array([np.cos(y_), np.sin(y_)]); F_ = sh_frame(sc_); lf_ = np.array([-fw_[1], fw_[0]])
    a_ = os.path.join(TELE_DIR, f"fsc_{tag}_top.jpg"); close(a_, np.r_[F_["c"] - fw_ * 0.30, F_["z"] + 1.1], np.r_[F_["c"] - fw_ * 0.12, F_["z"]], "AI-operated | bar from above")
    b_ = os.path.join(TELE_DIR, f"fsc_{tag}_side.jpg"); close(b_, np.r_[F_["c"] - lf_ * 0.9 - fw_ * 0.15, F_["z"] + 0.15], np.r_[F_["c"] - fw_ * 0.08, F_["z"]], "AI-operated | bar from the robot's right")
    print("VIEWS", a_, b_, "LOOK", look3("fsc_" + tag), flush=True)


def mem():
    try:
        import psutil as _ps
        return round(_ps.Process().memory_info().private / 2 ** 30, 2)
    except Exception as ex_:
        return str(ex_)[:60]


print("[fsc lib] loaded, kit private GB", mem(), flush=True)


def wrist(s_="right"):
    q_ = arm_lim(s_)
    return {k_: q_[k_] for k_ in ("wrist_roll", "wrist_pitch", "wrist_yaw")}


def mv(tag, **kw):
    """One carrying move (the skill's sh_move), AI-operated: the record, the seats, the wheel's clearance, a look."""
    mon_start(target=sc_); MON["t_max"] = 6000.0
    MON["held"] = {s_: sc_ for s_ in SIDES}; MON["target"] = None; MON["start"].pop(sc_, None)
    try:
        r_ = sh_move(sc_, tag=tag, **kw)
        w_ = sh_wheel(sc_)
        print(f"[mv {tag}] {kw} -> at {r_['at']} yaw {r_['yaw']} bar {r_['bar']} bar_rel {r_['bar_rel']} tilt {r_['tilt']} seat", {s_: (r_['seat'][s_]['seat_mm'], r_['seat'][s_]['pitch'], r_['seat'][s_]['lower_N']) for s_ in SIDES},
              "along", r_["along"], "wheel clear mm", round((w_["z"] - w_["r"]) * 1000, 1), "floor", sh_on_floor(sc_), "wristR", wrist("right"), "touch", r_["touch"], "rec", rec.n, flush=True)
        print(f"[mv {tag}] LOOK", r_["look"], flush=True)
        return r_
    except Abort as ex_:
        print(f"[mv {tag}] ABORT", str(ex_)[:400], "fallen", fallen(), "touch", {s_: sum(finger_touch(s_, sc_).values()) for s_ in SIDES}, "contacts", contact_report(), "rec", rec.n, flush=True)
        print(f"[mv {tag}] LOOK", look3("fsc_abort_" + tag), flush=True)
        return None


def topview(tag, h=2.38):
    p_, y_ = base(); F_ = sh_frame(sc_); c_ = (p_[:2] + F_["c"]) / 2
    a_ = os.path.join(TELE_DIR, f"fsc_{tag}_map.jpg"); close(a_, np.r_[c_ + np.array([0.0, -0.05]), h], np.r_[c_, 0.0], f"AI-operated | from above (north up), centre {np.round(c_, 2).tolist()}")
    print("TOP", a_, flush=True)


def mvto(tag, turn=0.0, to=None, step=0.15):
    """One carrying move: turn (deg, <= 15), then a step of at most `step` m toward the place `to` (world), heading kept."""
    p_, y_ = base(); kw_ = {}
    if abs(turn) > 0.5:
        kw_["turn"] = float(np.clip(turn, -15.0, 15.0))
    if to is not None:
        loc_ = RM.rz(y_ + np.radians(kw_.get("turn", 0.0)))[:2, :2].T @ (np.asarray(to, float) - p_[:2]); n_ = float(np.linalg.norm(loc_))
        if n_ > 0.02:
            loc_ = loc_ * min(1.0, step / n_); kw_["fwd"] = float(loc_[0]); kw_["side"] = float(loc_[1])
    return mv(tag, **{k_: round(v_, 4) for k_, v_ in kw_.items()})


def latc(want=-0.27, tol=0.02, speed=0.03):
    """Both hands together sideways (robot frame) until the bar is `want` m to the left of the pelvis line (- = right):
    the side steps left the bar 5 cm further right than taken and the cross-body left pad slid outward along it."""
    st_ = sh_state(sc_); dy_ = float(want - st_["bar_rel"][1])
    if abs(dy_) < tol:
        return dict(moved=0.0, bar_rel=st_["bar_rel"])
    dy_ = float(np.clip(dy_, -0.06, 0.06))
    p_, y_ = base(); l_ = np.array([-np.sin(y_), np.cos(y_), 0.0]); seat_ = sh_seat(sc_)
    PRE_ACTION("fsc_lat_recentre", dict(dy=round(dy_, 3)))
    both_move({s_: pad_mid(s_) + l_ * dy_ for s_ in SIDES}, sh_level_Q({s_: seat_[s_]["pitch"] for s_ in SIDES}), speed=speed, tol=0.006)
    op.run(0.5)
    st_ = sh_state(sc_)
    print("[latc] moved", round(dy_, 3), "bar_rel", st_["bar_rel"], "along", st_["along"], "seat", {s_: v_["seat_mm"] for s_, v_ in sh_seat(sc_).items()}, "touch", st_["touch"], "why", MON.get("why"), flush=True)
    return dict(moved=dy_, bar_rel=st_["bar_rel"])


def lslide(want=0.095, max_d=0.03, speed=0.02):
    """The LEFT pad alone along the bar back toward its place (`want` m left of the bar's middle): at every turn the
    cross-body left hand lagged and its pad slid ~3.5 mm outward along the bar (0.097 -> 0.118 in six moves; the bar's
    end is at 0.15). The right hand keeps still and holds the bar."""
    F_ = sh_frame(sc_); st_ = sh_state(sc_); a_ = float(st_["along"]["left"])
    dd_ = float(np.clip(a_ - want, -max_d, max_d))
    if abs(dd_) < 0.006:
        return dict(moved=0.0, along=st_["along"])
    seat_ = sh_seat(sc_)
    PRE_ACTION("fsc_left_slide", dict(d=round(dd_, 3)))
    Q_ = sh_level_Q({s_: seat_[s_]["pitch"] for s_ in SIDES})
    both_move({"left": pad_mid("left") - np.r_[F_["lft"] * dd_, 0.0], "right": pad_mid("right").copy()}, Q_, speed=speed, tol=0.004)
    op.run(0.5)
    st_ = sh_state(sc_)
    print("[lslide] asked", round(dd_, 3), "along", st_["along"], "seat", {s_: v_["seat_mm"] for s_, v_ in sh_seat(sc_).items()}, "pad_to_bar", st_["pad_to_bar"], "touch", st_["touch"], "bar_rel", st_["bar_rel"], "tilt", st_["tilt"], "why", MON.get("why"), flush=True)
    return dict(moved=dd_, along=st_["along"])


def prepitch(left=-12.0, speed=0.03):
    """Before a carrying move: the left fingers pitched tips-down `left` deg where they are (the right as trimmed).
    Seen: with the bar toward the left palm the skill's trim (at most 8 deg) did not stop the creep while walking backward
    (-3.8 -> -6.1 -> -7.1 mm in two moves); the bar's weight along the pad passes the upper pad's friction only past ~8 deg."""
    seat_ = sh_seat(sc_)
    PRE_ACTION("fsc_prepitch", dict(left=left))
    both_move({s_: pad_mid(s_).copy() for s_ in SIDES}, sh_level_Q({"left": float(left), "right": float(seat_["right"]["pitch"])}), speed=speed, tol=0.006)
    op.run(0.5)
    s2_ = sh_seat(sc_)
    print("[prepitch] seat", {s_: (s2_[s_]["seat_mm"], s2_[s_]["pitch"]) for s_ in SIDES}, "touch", {s_: sum(finger_touch(s_, sc_).values()) for s_ in SIDES}, "why", MON.get("why"), flush=True)
    return s2_


SD = dict(hf=0.0)


def sd_rep(tag):
    st_ = sh_state(sc_); w_ = sh_wheel(sc_)
    print(f"[{tag}] pel", st_["pel"], "yaw", st_["yaw"], "bar", st_["bar"], "bar_rel", st_["bar_rel"], "tilt", st_["tilt"], "along", st_["along"], "pad_to_bar", st_["pad_to_bar"], "touch", st_["touch"],
          "seat", {s_: (v_["seat_mm"], v_["pitch"], v_["lower_N"], v_["upper_N"]) for s_, v_ in sh_seat(sc_).items()}, "wheel x", round(w_["x"], 3), "/", round(w_["x_up"], 3), "wheel z-r mm", round((w_["z"] - w_["r"]) * 1000, 1),
          "floor", sh_on_floor(sc_), "wristR", wrist("right"), "wristL", wrist("left"), "why", MON.get("why"), "rec", rec.n, flush=True)
    return st_, w_


def sd_touch():
    """The skill's own first step of the set-down (copied from sh_set_down_walk): hands down in 5 mm steps until the
    hanging rear wheel touches."""
    seat_ = sh_seat(sc_)
    for j_ in range(10):
        if sh_on_floor(sc_):
            break
        both_move({s_: pad_mid(s_) + np.array([0.0, 0.0, -0.005]) for s_ in SIDES}, sh_level_Q({s_: seat_[s_]["pitch"] for s_ in SIDES}), speed=0.02, tol=0.004)
        op.run(0.3)
        if MON.get("why"):
            raise Abort(MON["why"])
    return sd_rep("touch")


def sd_leg(tag, seg=0.12, v=0.05, trim=True):
    """ONE leg of the skill's set-down walk (copied from sh_set_down_walk's loop body): the robot walks `seg` forward while
    the hands bring the bar down along the arc round the planted rear wheel. Returns 'finish' when the legs are over."""
    b_ = sc_
    w_ = sh_wheel(b_)
    SD["hf"] = float(np.clip(w_["z"] - w_["r"], 0.0, 0.03))
    z_arc_ = w_["arc"](max(w_["x"], 0.0)) + SD["hf"]
    tilt_ = sh_state(b_)["tilt"]
    print(f"[leg {tag}] wheel {w_['x']:.3f} m from the bar line (upright {w_['x_up']:.3f}), wheel z {w_['z']:.3f} (floor {SD['hf']:.3f}), bar z {w_['bar_z']:.3f} arc {z_arc_:.3f}, tilt {tilt_}", flush=True)
    if w_["x"] > w_["x_up"] - 0.06 or tilt_ < 4.0 or len(sh_on_floor(b_)) >= 2:
        return "finish"
    if w_["bar_z"] > z_arc_ + 0.004:
        seat_ = sh_seat(b_)
        both_move({s_: pad_mid(s_) + np.array([0.0, 0.0, z_arc_ - 0.002 - w_["bar_z"]]) for s_ in SIDES}, sh_level_Q({s_: seat_[s_]["pitch"] for s_ in SIDES}), speed=0.02, tol=0.006)
        op.run(0.4)
        if MON.get("why"):
            raise Abort(MON["why"])
        w_ = sh_wheel(b_)
    step_ = float(min(seg, w_["x_up"] - w_["x"] + 0.01))
    gw_, gb_, deck_ = w_["geom"], w_["bar_geom"], sh_frame(b_)["deck"].copy()

    def vz_now(arc=w_["arc"], x_up=w_["x_up"], L=w_["L"]):
        x_ = float(np.clip((d.geom_xpos[gw_][:2] - d.geom_xpos[gb_][:2]) @ deck_, 0.0, x_up))
        vf_ = max(float(ts.loco.v_filt[0]), 0.0) if getattr(ts.loco, "moving", False) else 0.0
        ff_ = -x_ / max(float(np.sqrt(max(L ** 2 - x_ ** 2, 1e-6))), 1e-3) * vf_
        return float(np.clip(ff_ + 6.0 * (arc(x_) + SD["hf"] - 0.004 - float(d.geom_xpos[gb_][2])), -0.05, 0.01))
    hands_ = [(lambda n=n: dict(cmd="ee", name=n, mode="velocity", linear=[0.0, 0.0, vz_now()], frame="world", ttl=3 * op.period)) for n in SIDES]
    PRE_ACTION("sh_set_down_leg", dict(step=round(step_, 3)))
    ready_to_walk(tuple(SIDES))
    p0_, y0_ = base()
    g_ = p0_[:2] + RM.rz(y0_)[:2, :2] @ np.array([step_, 0.0])
    _leg_by_anchor_xy(g_, hands_, (v, 0.04))
    if MON.get("why"):
        raise Abort(MON["why"])
    if fallen():
        raise Abort("fell")
    sd_rep(f"leg {tag} walked {step_:.3f}")
    ok_, t_, e_, a_ = sh_in_jaws(b_)
    if not all(t_[s_] > 0 for s_ in SIDES):
        raise Abort(f"a jaw pair lost the bar in the set-down: {t_}")
    if trim and sh_state(b_)["tilt"] > 1.5:
        sh_trim(b_, seat_max=13.5)
        sd_rep(f"leg {tag} trimmed")
    return "leg"
