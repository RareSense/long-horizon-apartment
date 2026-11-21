r"""Does the apartment LOOK clean at the end of a run? A number and a list, not an opinion (offline, no simulator).

    py -3.12 C:\Users\raresense\sim_home\apartment\full_plan\check_clean_look.py RUN_FOLDER [--targets clean_targets_v3.json] [--out FILE.json]

Reads, from the run folder the runner wrote (E:\urc_home\scripts\home\episode.py): room.json (the room file used),
state_rec.npz (t, qpos of the merged model, 10-25 Hz) and result.json (events: garments are cloth and are not in qpos).
Reads clean_targets_v3.json (make_full_plan_v3.py): for every loose thing of the pack what "clean" means
(in_container / on_surface / at_spot / stay / known_mess). Writes nothing unless --out is given.

How the qpos columns are matched to bodies (state_rec.npz has no names): every 7-number block that is a free joint
(unit quaternion) is matched, by its position in the FIRST row, to the start positions of the loose things (pack body
origins, world = scene - (0.90, 0.45)) and of the room's extras (bin, hamper); one-to-one, nearest first, within 6 cm
in x/y. A thing of the pack with no matching block was NOT loose in that room (static or frozen): it is where it started.

"Start" for the stay checks = the last row before the robot's pelvis first moved 3 cm (the scene has settled by then;
the light saber slides about 25 cm in the first seconds).
Positions are body origins (the free joint's qpos). Pure numpy + json; well under 0.5 GB."""
import sys, os, json, math, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def quat_mat(q):
    w, x, y, z = q / max(np.linalg.norm(q), 1e-12)
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def yaw_of(q):
    R = quat_mat(q); return math.degrees(math.atan2(R[1, 0], R[0, 0]))


def tilt_of(q):
    return math.degrees(math.acos(max(-1.0, min(1.0, quat_mat(q)[2, 2]))))


def ang_diff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


def free_blocks(row):
    """Indices i where row[i:i+7] looks like a free joint (position + unit quaternion), robot base excluded later."""
    out = []
    for i in range(0, len(row) - 6):
        qn = float(np.linalg.norm(row[i + 3:i + 7]))
        if abs(qn - 1.0) < 2e-3 and abs(float(row[i + 2])) < 3.0:
            out.append(i)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--targets", default=os.path.join(HERE, "clean_targets_v3.json"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--match-tol", type=float, default=0.06)
    a = ap.parse_args()
    CT = json.load(open(a.targets, encoding="utf-8")); OBJS = CT["objects"]; S0 = np.array(CT["start_offset_scene"], float)
    room = json.load(open(os.path.join(a.run, "room.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(a.run, "result.json"), encoding="utf-8")) if os.path.exists(os.path.join(a.run, "result.json")) else {}
    z = np.load(os.path.join(a.run, "state_rec.npz")); t = z["t"]; Q = z["qpos"]
    q0, qN = Q[0].astype(float), Q[-1].astype(float)
    # ---- the robot: its floating base is the first block (pelvis about 0.75-0.8 m up at the start pose)
    base0 = q0[:3]
    moved = np.where(np.linalg.norm(Q[:, :2].astype(float) - base0[:2], axis=1) > 0.03)[0]
    k_ref = max(0, int(moved[0]) - 1) if len(moved) else 0
    qR = Q[k_ref].astype(float)
    # ---- candidates: loose things of the pack + the room's extras, at their start (world)
    cand = {n: np.array(e["start_world"], float) for n, e in OBJS.items()}
    for ex in room.get("extras", []):
        p = np.array(ex.get("pose", [0, 0, 0])[:2], float) - S0
        cand[ex["name"]] = np.array([p[0], p[1], float(ex.get("z", 0.0))])
    blocks = [i for i in free_blocks(q0) if i >= 7]
    pairs = sorted((float(np.linalg.norm(q0[i:i + 2] - c[:2])), i, n) for i in blocks for n, c in cand.items()
                   if np.linalg.norm(q0[i:i + 2] - c[:2]) < a.match_tol and abs(q0[i + 2] - c[2]) < 0.45)
    col, used = {}, set()
    for dist, i, n in pairs:
        if n in col or i in used:
            continue
        col[n] = i; used.update(range(i, i + 7))
    unmatched = [i for i in blocks if i not in used and not any(j in used for j in range(i, i + 7))]

    def pose(n, row):
        if n in col:
            i = col[n]; return row[i:i + 3].copy(), row[i + 3:i + 7].copy()
        e = OBJS.get(n)
        if e is None:
            return None, None
        return np.array(e["start_world"], float), np.array(e["start_quat_wxyz"], float)
    garments_ok = {ev.get("obj") for ev in res.get("events", []) if ev.get("ev") == "tidy_garment" and ev.get("ok")}
    cloth_in_room = set(room.get("structure", {}).get("cloth", []) or [])
    conts = CT["containers"]; surfs = CT["surfaces"]
    rows = []
    for n, e in sorted(OBJS.items()):
        ex = e["expect"]; kind = ex["kind"]; loose = n in col
        r = dict(name=n, cls=e["cls"], kind=kind, loose_in_run=loose, ok=None, why="")
        if e.get("cloth") and n in cloth_in_room:
            if kind in ("in_container", "at_spot", "on_surface"):
                r["ok"] = n in garments_ok
                r["why"] = "cloth (not in state_rec): " + ("result.json says tidy_garment ok (not checked from the state)" if r["ok"] else "no successful tidy_garment in result.json")
            else:
                r["ok"] = kind != "known_mess"; r["why"] = "cloth (not in state_rec): " + ex.get("why", "")
            rows.append(r); continue
        p, q = pose(n, qN); pr, qr = pose(n, qR)
        if p is None:
            r["ok"] = False; r["why"] = "no pose"; rows.append(r); continue
        r["final_world"] = [round(float(v), 3) for v in p]
        if kind == "stay" or kind == "known_mess":
            dxy = float(np.linalg.norm(p[:2] - pr[:2])); dz = abs(float(p[2] - pr[2])); dt = abs(tilt_of(q) - tilt_of(qr))
            within = dxy <= ex.get("tol_xy_m", 0.05) and dz <= ex.get("tol_z_m", 0.05) and dt <= ex.get("max_tilt_change_deg", 10.0)
            if kind == "stay":
                r["ok"] = bool(within)
                r["why"] = "in place" if within else f"moved {100 * dxy:.0f} cm / {100 * dz:.0f} cm up-down / tilted {dt:.0f} deg since the task began (knocked or pushed)"
            else:
                r["ok"] = False
                r["why"] = "known mess the plan cannot tidy: " + ex.get("why", "") + ("" if within else f" (and it moved {100 * dxy:.0f} cm)")
        elif not loose:
            r["ok"] = False; r["why"] = "planned to move, but it is not loose in this run's room (static there): still where it started"
        elif kind == "in_container":
            c = conts[ex["container"]]
            if c.get("movable"):
                cp, cq = pose(ex["container"], qN); cs_p, cs_q = pose(ex["container"], q0)
                if cp is None:
                    r["ok"] = False; r["why"] = f"container {ex['container']} not found"; rows.append(r); continue
                Rrel = quat_mat(cq) @ quat_mat(cs_q).T
                loc = Rrel.T @ (p - cp)
                inside = bool(np.all(loc >= np.array(c["lo_off"]) - 0.01) and np.all(loc <= np.array(c["hi_off"]) + 0.01))
            else:
                rc = c["rect_scene"]; cc = np.array(rc["c"], float) - S0; yw = math.radians(rc["yaw_deg"])
                Rm = np.array([[math.cos(yw), -math.sin(yw)], [math.sin(yw), math.cos(yw)]])
                loc = Rm.T @ (p[:2] - cc)
                inside = bool(np.all(np.abs(loc) <= np.array(rc["h"], float) + 0.01) and c["z"][0] <= p[2] <= c["z"][1])
            r["ok"] = inside; r["why"] = f"inside {ex['container']}" if inside else f"not inside {ex['container']}"
        elif kind == "on_surface":
            s = surfs[ex["surface"]]; lo = np.array(s["lo_scene"], float) - S0; hi = np.array(s["hi_scene"], float) - S0
            on = bool(np.all(p[:2] >= lo - 0.01) and np.all(p[:2] <= hi + 0.01) and s["z"][0] <= p[2] <= s["z"][1])
            r["ok"] = on; r["why"] = f"on {ex['surface']}" if on else f"not on {ex['surface']} (z {p[2]:.2f} m)"
            if ex.get("spot_scene"):
                r["dist_to_spot_m"] = round(float(np.linalg.norm(p[:2] - (np.array(ex["spot_scene"], float) - S0))), 3)
        elif kind == "at_spot":
            sp = np.array(ex["spot_world"], float); dxy = float(np.linalg.norm(p[:2] - sp))
            ok = dxy <= ex["tol_xy_m"]; why = [f"{100 * dxy:.0f} cm from its spot (tolerance {100 * ex['tol_xy_m']:.0f} cm)"]
            if ex.get("yaw_deg") is not None:
                dy = ang_diff(yaw_of(q), ex["yaw_deg"])
                ok = ok and dy <= ex.get("tol_yaw_deg", 25.0); why.append(f"yaw off by {dy:.0f} deg")
            if ex.get("upright_max_tilt_deg") is not None:
                tl = tilt_of(q); ok = ok and tl <= ex["upright_max_tilt_deg"]; why.append(f"tilt {tl:.0f} deg")
            r["ok"] = bool(ok); r["why"] = ", ".join(why)
        rows.append(r)
    # doors the pack leaves open: a frozen joint stays open
    unfrozen = set(room.get("structure", {}).get("unfreeze", []) or [])
    frozen = bool(room.get("structure", {}).get("freeze_joints", False))
    doors = []
    for dd in CT.get("open_doors", []):
        if frozen and dd["name"] not in unfrozen:
            doors.append(dict(name=dd["name"], ok=False, why="frozen open in this room (the pack leaves it open)"))
        else:
            doors.append(dict(name=dd["name"], ok=None, why="free in this room: its joint is not mapped from state_rec (look at the end frame)"))
    checked = [r for r in rows if r["ok"] is not None]
    n_ok = sum(1 for r in checked if r["ok"]); bad = [r for r in checked if not r["ok"]]
    by = {}
    for r in bad:
        by.setdefault(r["kind"], []).append(r)
    summary = dict(run=os.path.abspath(a.run), targets=os.path.abspath(a.targets), rows_in_state=int(len(t)), t_end_s=round(float(t[-1]), 1), task_start_row=k_ref,
                   task_start_t_s=round(float(t[k_ref]), 2), loose_bodies_matched=len(col), free_blocks_unmatched=unmatched,
                   clean_fraction=round(n_ok / max(1, len(checked)), 3), clean=n_ok, checked=len(checked), not_clean=len(bad),
                   not_clean_by_kind={k: len(v) for k, v in by.items()}, doors_not_closed=[d_["name"] for d_ in doors if d_["ok"] is False],
                   fell=res.get("fell"), note="planned things (in_container / on_surface / at_spot) are clean only at their destination; stay things only if not knocked; "
                                              "known_mess counts as not clean; cloth from result.json events only")
    print(f"LOOKS CLEAN: {n_ok} of {len(checked)} loose things ({100 * summary['clean_fraction']:.0f} %); NOT clean: {len(bad)}; doors still open: {len(summary['doors_not_closed'])}")
    print(f"  run {summary['run']}  (t_end {summary['t_end_s']} s, task began at row {k_ref}, t {summary['task_start_t_s']} s; {len(col)} loose bodies matched"
          + (f", {len(unmatched)} free blocks unmatched" if unmatched else "") + (", the robot FELL" if res.get("fell") else "") + ")")
    order = ("at_spot", "in_container", "on_surface", "stay", "known_mess")
    for k in order:
        for r in sorted(by.get(k, []), key=lambda r_: r_["name"]):
            print(f"  NOT CLEAN [{k}] {r['name']} ({r['cls']}): {r['why']}" + (f"  final {r['final_world']}" if r.get("final_world") else ""))
    for d_ in doors:
        if d_["ok"] is not True:
            print(f"  DOOR {d_['name']}: {d_['why']}")
    if a.out:
        json.dump(dict(summary=summary, not_clean=bad, doors=doors, all=rows), open(a.out, "w", encoding="utf-8"), indent=1)
        print("written", a.out)


if __name__ == "__main__":
    main()
