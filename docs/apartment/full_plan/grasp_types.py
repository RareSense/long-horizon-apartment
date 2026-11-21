"""Candidate grasps of the G1's Unitree Dex1-1 two-jaw gripper, from an object's surface points. Pure numpy.

EVERYTHING HERE IS BY GEOMETRY, NOT VERIFIED in simulation. The live agents confirm or reject each type.

Five grasp types (README_GRASPS.md says exactly what each assumes):
  top_down       jaws come straight down fully open over a section and close horizontally (the floor agent's search,
                 E:/urc_home/src/urc/tasks/home/grasp_geom.py find(), copied unchanged as section_search())
  surface_pinch  the same, but the fingertips go down to 1.5 mm above the support (floor or table) and slide on it while
                 closing: low things 1.0-4 cm high (crumpled paper, a bag, a flat pouch's edge)
  side           hand level, fingers horizontal, jaws close horizontally on an upright thing's section at height zm
  rim_pinch      jaws part-open (wall + 1 cm), one jaw inside a cup / glass / bowl, one outside, closing on the wall
                 (needs the HOLLOW collider of hollow_colliders.json in the room; the pack's own collider is solid)
  edge           fingers horizontal, jaws close VERTICALLY on the part of a flat thing that overhangs a table edge (lower
                 jaw under it); if it does not overhang, it is first slid to the edge (slide_m) by a fingertip press

Points are world (scene) frame, metres, Z up. Each candidate is a dict:
  type, verdict ('yes' | 'marginal'), point [x, y, z] (middle between the pads), close [x, y, z] (unit closing direction),
  approach [x, y, z] (unit direction the hand moves in at the end), jaw_gap_m (opening to come in with), width_m
  (material between the pads), bite_m, pad_bottom_above_support_m, score (lower is better), notes [str], needs [str]

Reading the precomputed table (grasps_v2.json, made by make_grasps_v2.py):
    import sys; sys.path.insert(0, r"C:/Users/raresense/sim_home/apartment/full_plan")
    import grasp_types as GT
    T = GT.load()                                    # {display name: entry}
    GT.best(T, "r183i1_cup")                         # best candidate over all types (or type="rim_pinch")
    GT.candidates(T, "r183i1_cup", "side")           # all side candidates, best first
The scene frame is the pack's; the episode world frame is scene - (0.90, 0.45): GT.to_world(p)."""
from __future__ import annotations

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASIS = "by geometry, not verified"
START = np.array([0.90, 0.45])             # robot start in the scene frame; world = scene - START

# Dex1-1 on the G1 (E:/urc_home/scripts/towel_prep/build_g1_dex1.py and the dex1_1 URDF meshes, measured 18 Nov):
DEX1 = dict(
    open_gap=0.079,        # between the pad faces, fully open (model; the task text says 8.2 cm)
    pad_w=0.029,           # pad across the finger
    pad_l=0.029,           # pad along the finger (its "height" when the fingers point down)
    pad_t=0.0115,          # pad thickness
    jaw_t=0.015,           # jaw body behind a pad face (the floor agent's sweep allowance)
    finger_half_h=0.0196,  # half the finger plate's width across the finger (3.9 cm)
    palm=0.062,            # pad middle to the gripper base's front face (the floor agent's max_palm)
    base_half_h=0.031,     # gripper base: 6.2 cm across the closing direction ...
    base_half_w=0.029,     # ... and 5.8 cm along it, 7.4 cm long
    squeeze_n=6.0,         # measured squeeze per pad in the floor agent's runs
    squeeze_max_n=20.0,    # the jaw motor's limit in the model (ctrlrange)
    mu=1.2)                # pad friction in the model
CLEAR = 0.0045                             # clearance a side the floor agent's search keeps (7.0 cm widest section)
G = 9.81


# ------------------------------------------------------------------ the floor agent's top-down section search (unchanged)
def section_search(points, z_support, open_gap=DEX1["open_gap"], clearance=CLEAR, pad_w=DEX1["pad_w"], pad_h=DEX1["pad_l"], floor_clear=0.006, min_bite=0.008,
                   n_dir=18, step=0.01, max_palm=DEX1["palm"]):
    """Copy of grasp_geom.find() (E:/urc_home, commit c2467f3): sections the open jaws can come straight down over."""
    P = np.asarray(points, float)
    c0 = P[:, :2].mean(0)
    out = []
    wmax = open_gap - 2 * clearance
    for k in range(n_dir):
        a = np.pi * k / n_dir
        u = np.array([np.cos(a), np.sin(a)]); v = np.array([-u[1], u[0]])
        pu = P[:, :2] @ u; pv = P[:, :2] @ v
        for s in np.arange(pv.min() + pad_w / 2 - 0.004, pv.max() - pad_w / 2 + 0.004 + 1e-9, step):
            win = np.abs(pv - s) <= pad_w / 2 + 0.003
            if win.sum() < 3:
                continue
            ztop = P[win, 2].max()
            for zg in sorted({max(z_support + floor_clear + pad_h / 2, ztop - 0.012), max(z_support + floor_clear + pad_h / 2, ztop - 0.03),
                              z_support + floor_clear + pad_h / 2}):
                zlow = zg - pad_h / 2
                if ztop - zlow < min_bite or ztop - zg > max_palm:
                    continue
                above = win & (P[:, 2] > zlow)
                if above.sum() < 3:
                    continue
                a0, a1 = pu[above].min(), pu[above].max()
                w = a1 - a0
                if w > wmax or w < 0.002:
                    continue
                mid_u = (a0 + a1) / 2
                sweep = (np.abs(pu - mid_u) > w / 2 + 0.002) & (np.abs(pu - mid_u) <= open_gap / 2 + 0.016) & (np.abs(pv - s) <= pad_w / 2 + 0.012) & (P[:, 2] > zlow)
                if sweep.any():
                    continue
                band = above & (P[:, 2] < zg + pad_h / 2)
                bite = float(min(ztop, zg + pad_h / 2) - zlow)
                pt2 = u * mid_u + v * s
                off = float(np.linalg.norm(pt2 - c0))
                score = w + 0.5 * off - 0.5 * min(bite, pad_h) + (0.0 if band.sum() >= 3 else 0.05)
                out.append(dict(point=np.r_[pt2, zg], close=np.r_[u, 0.0], width=float(w), z=float(zg), top=float(ztop), bite=bite, off_centre=off, score=float(score)))
    out.sort(key=lambda g: g["score"])
    return out


def _cand(type_, verdict, point, close, approach, gap, width, bite, pad_bottom, score, notes=(), needs=(), **extra):
    d = dict(type=type_, verdict=verdict, point=[round(float(v), 4) for v in point], close=[round(float(v), 4) for v in close],
             approach=[round(float(v), 4) for v in approach], jaw_gap_m=round(float(gap), 4), width_m=round(float(width), 4), bite_m=round(float(bite), 4),
             pad_bottom_above_support_m=round(float(pad_bottom), 4), score=round(float(score), 4), notes=list(notes), needs=list(needs), basis=BASIS)
    d.update({k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in extra.items()})
    return d


def _one_per_direction(cands, key="close", bins=12, half_turn=True, keep=8):
    """The best candidate per closing (or approach) direction sector."""
    seen = {}; out = []
    for c in sorted(cands, key=lambda c: c["score"]):
        a = math.atan2(c[key][1], c[key][0])
        k = int(round(a / (math.pi if half_turn else 2 * math.pi) * bins)) % bins
        if k in seen:
            continue
        seen[k] = 1; out.append(c)
        if len(out) >= keep:
            break
    return out


# ------------------------------------------------------------------ 1 top-down (existing)
def top_down(points, z_support, mass=0.0):
    G_ = section_search(points, z_support)
    tight = False
    if not G_:
        G_ = section_search(points, z_support, clearance=0.0005); tight = bool(G_)
    out = []
    for g in G_:
        notes = []; v = "yes"
        if tight:
            v = "marginal"; notes.append(f"{100 * g['width']:.1f} cm across: under 4.5 mm to spare a side (the floor agent's search rejects it)")
        if g["off_centre"] > 0.08 and mass >= 0.2:
            v = "marginal"; notes.append(f"section {100 * g['off_centre']:.0f} cm off the middle: it can swing or tip in the jaws")
        out.append(_cand("top_down", v, g["point"], g["close"], [0, 0, -1], DEX1["open_gap"], g["width"], g["bite"], g["z"] - DEX1["pad_l"] / 2 - z_support, g["score"],
                         notes, ["floor_pick / surface pick, fingers down (exists for the floor: run 1118_193303)"], off_centre_m=g["off_centre"], top_m=g["top"]))
    return _one_per_direction(out)


# ------------------------------------------------------------------ 2 surface-level pinch
def surface_pinch(points, z_support, mass=0.0):
    """Fingertips 1.5 mm above the support (they slide on it while closing). Height of the thing above the support:
    1.5 cm and more 'yes', 1.0-1.5 cm 'marginal', under 1.0 cm none (nothing for the pads)."""
    P = np.asarray(points, float)
    h = float(P[:, 2].max() - z_support)
    if h < 0.010 or h > 0.06:
        return []
    G_ = section_search(P, z_support, floor_clear=0.0015, min_bite=0.006)
    tight = False
    if not G_:
        G_ = section_search(P, z_support, floor_clear=0.0015, min_bite=0.006, clearance=0.0005); tight = bool(G_)
    out = []
    for g in G_:
        v = "yes" if h >= 0.015 and not tight else "marginal"
        notes = [f"{100 * h:.1f} cm high: fingertips at the support, {100 * g['bite']:.1f} cm of pad on it"]
        if tight:
            notes.append(f"{100 * g['width']:.1f} cm across: under 4.5 mm to spare a side")
        out.append(_cand("surface_pinch", v, g["point"], g["close"], [0, 0, -1], DEX1["open_gap"], g["width"], g["bite"], 0.0015, g["score"], notes,
                         ["fingertips pressed lightly on the support and kept there while the jaws close (new posture: hand 1.5 mm off the floor / table)"],
                         off_centre_m=g["off_centre"]))
    return _one_per_direction(out)


# ------------------------------------------------------------------ 3 side grasp
def _pitch_needed(dz_room):
    """Hand pitched down by th (fingers toward the support): the base's lower front edge, `palm` behind the pad middle
    and base_half_h below it, rises by palm*sin(th). Smallest th (deg) giving dz_room (pad middle - support - 5 mm)."""
    for th in range(0, 36, 1):
        t = math.radians(th)
        if -DEX1["base_half_h"] * math.cos(t) + DEX1["palm"] * math.sin(t) + dz_room >= 0:
            return th
    return None


def side(points, z_support, com=None, mass=0.0, n_head=24, dz=0.01):
    P = np.asarray(points, float)
    if not len(P):
        return []
    com = P.mean(0) if com is None else np.asarray(com, float)
    top = float(P[:, 2].max())
    zmin = z_support + max(DEX1["pad_w"] / 2 + 0.006, DEX1["finger_half_h"] + 0.001)
    out = []
    og, jt, pl, pw = DEX1["open_gap"], DEX1["jaw_t"], DEX1["pad_l"], DEX1["pad_w"]
    for k in range(n_head):
        phi = 2 * math.pi * k / n_head
        a = np.array([math.cos(phi), math.sin(phi)]); u = np.array([-a[1], a[0]])
        pa = P[:, :2] @ a; pu = P[:, :2] @ u
        for zm in np.arange(zmin, top - 0.006 + 1e-9, dz):
            fb = np.abs(P[:, 2] - zm) <= DEX1["finger_half_h"]
            if fb.sum() < 5:
                continue
            pb = fb & (np.abs(P[:, 2] - zm) <= pw / 2)
            if pb.sum() < 5:
                continue
            a_near = pa[fb].min()
            mids = sorted({round(a_near + pl / 2 + 0.003, 4), round((pa[fb].min() + pa[fb].max()) / 2, 4), round(a_near + DEX1["palm"] - 0.008, 4)})
            for am in mids:
                W = pb & (np.abs(pa - am) <= pl / 2)
                if W.sum() < 3:
                    continue
                u0, u1 = pu[W].min(), pu[W].max(); w = u1 - u0; c = (u0 + u1) / 2
                if w > og - 0.001 or w < 0.003:
                    continue
                # fingers (tip to palm) meet nothing wider than the section; the palm meets nothing
                along = fb & (pa <= am + pl / 2) & (pa >= am - DEX1["palm"])
                if (along & (np.abs(pu - c) > w / 2 + 0.002) & (np.abs(pu - c) <= og / 2 + jt)).any():
                    continue
                palm = (np.abs(P[:, 2] - zm) <= DEX1["base_half_h"]) & (pa < am - DEX1["palm"] + 0.003) & (np.abs(pu - c) <= DEX1["base_half_w"] + 0.003)
                if palm.any():
                    continue
                th = _pitch_needed(zm - z_support - 0.005)
                if th is None:
                    continue
                bite = float(min(P[W, 2].max(), zm + pw / 2) - max(P[W, 2].min(), zm - pw / 2))
                if bite < 0.008:
                    continue
                pt = a * am + u * c
                off = float(np.linalg.norm(pt - com[:2]))
                v = "yes"; notes = [f"section {100 * w:.1f} cm across at {100 * (zm - z_support):.1f} cm above the support (pad middle)"]
                needs = ["side grasp: hand level, fingers horizontal (new skill)"]
                if w > og - 2 * CLEAR:
                    v = "marginal"; notes.append("under 4.5 mm to spare a side")
                if th > 0:
                    v = "marginal"; notes.append(f"the gripper base would touch the support with a level hand: pitch the hand down about {th} deg")
                if mass > 0.2 and zm < com[2] - 0.03:
                    notes.append("held below its centre of mass: it can tip in the jaws when lifted fast")
                score = w + 0.5 * off + 0.2 * max(0.0, com[2] - zm) + 0.002 * th - 0.2 * bite
                out.append(_cand("side", v, np.r_[pt, zm], np.r_[u, 0.0], np.r_[a, 0.0], og, w, bite, zm - pw / 2 - z_support, score, notes, needs,
                                 pitch_down_deg=th, height_above_support_m=zm - z_support, heading_deg=round(math.degrees(phi)) % 360))
    return _one_per_direction(out, key="approach", bins=12, half_turn=False, keep=12)


# ------------------------------------------------------------------ 4 rim pinch
def rim_pinch(vis_points, z_support, cav, axis_R, origin, mass=0.0, hollow=False, n_az=24, clr=0.005):
    """vis_points: the VISUAL mesh points (hollow). cav: the opening found by make_hollow_colliders.cavity() in the axis
    frame axis_R (columns: the frame's x, y, z in the world; z = out of the opening), origin: that frame's origin.
    One jaw inside at the wall, one outside, opening = wall in the pad band + 2 x clr."""
    Q = (np.asarray(vis_points, float) - origin) @ axis_R
    c = np.asarray(cav["c"], float)
    jt, pl, pw, og = DEX1["jaw_t"], DEX1["pad_l"], DEX1["pad_w"], DEX1["open_gap"]
    d = Q[:, :2] - c
    out = []
    for k in range(n_az):
        th = 2 * math.pi * k / n_az
        u = np.array([math.cos(th), math.sin(th)]); v = np.array([-u[1], u[0]])
        r = d @ u; s = d @ v
        S = np.abs(s) <= pw / 2 + 0.003
        near = S & (r > 0)
        if near.sum() < 5:
            continue
        z_rim = float(Q[near, 2].max())
        best = None
        for bite in (0.025, 0.02, 0.015, 0.01):
            zl = z_rim - bite
            band = near & (Q[:, 2] >= zl)
            r_in, r_out = float(r[band].min()), float(r[band].max())
            w = r_out - r_in
            if r_in < 0.012 or w + 2 * clr > og:
                continue
            win = np.abs(s) <= pw / 2 + 0.006
            inner = win & (Q[:, 2] >= zl) & (r >= r_in - clr - jt) & (r <= r_in - clr)
            outer = win & (Q[:, 2] >= zl) & (r >= r_out + clr) & (r <= r_out + clr + jt)
            if inner.any() or outer.any():
                continue
            back = win & (Q[:, 2] >= zl) & (r < r_in - clr - jt)
            clear_in = float((r_in - clr - jt) - r[back].max()) if back.any() else float(r_in - clr - jt + cav["r_rim_in"])
            # outer jaw's tip must stay above the support (world)
            tip_out = origin + axis_R @ np.r_[c + u * (r_out + clr + jt / 2), zl]
            if tip_out[2] < z_support + 0.004:
                continue
            wall_top = (np.abs(s) <= 0.003) & (r > 0) & (Q[:, 2] >= z_rim - 0.005)       # the wall itself, on the pad's centre line
            if wall_top.sum() < 2:
                wall_top = near & (Q[:, 2] >= z_rim - 0.005)
            wall_t = float(r[wall_top].max() - r[wall_top].min())
            cu = (r_in + r_out) / 2
            moment = mass * G * cu
            cap6, cap20 = DEX1["squeeze_n"] * bite, DEX1["squeeze_max_n"] * bite
            score = w + 0.4 * (pl - bite) + (0.05 if moment > cap6 else 0.0) + (0.05 if moment > cap20 else 0.0)
            if best is None or score < best[0]:
                best = (score, bite, zl, r_in, r_out, w, clear_in, wall_t, cu, moment, cap6, cap20)
        if best is None:
            continue
        score, bite, zl, r_in, r_out, w, clear_in, wall_t, cu, moment, cap6, cap20 = best
        pm_ax = np.r_[c + u * cu, zl + pl / 2]
        point = origin + axis_R @ pm_ax
        close = axis_R @ np.r_[u, 0.0]
        approach = -axis_R[:, 2]
        notes = [f"wall {1000 * wall_t:.0f} mm at the rim ({100 * w:.1f} cm across the 2.9 cm pad band: wall + the rim's curve), jaws open {100 * (w + 2 * clr):.1f} cm, "
                 f"{100 * bite:.1f} cm of pad on it, {100 * clear_in:.1f} cm clear inside behind the inner jaw"]
        v = "yes" if hollow else "no"
        needs = ["rim pinch: jaws stopped part-open at the opening given (new skill)"]
        if hollow:
            needs.append("the hollow collider of hollow_colliders.json applied in the room (the pack's collider is a solid hull)")
        else:
            notes.append("the collider is the pack's solid hull: the inner jaw cannot enter; no hollow collider made for this one")
        if moment > cap6:
            v = "marginal" if v == "yes" else v
            notes.append(f"held at the rim the weight turns it {moment:.2f} N m; the pads resist about {cap6:.2f} N m at 6 N" + (f" ({cap20:.2f} at 20 N)" if moment <= cap20 else ": it will swing to hang from the grip"))
        if abs(axis_R[2, 2]) < 0.9:
            v = "marginal" if v == "yes" else v
            notes.append("the opening faces sideways: the hand comes in level along the axis")
        out.append(_cand("rim_pinch", v, point, close, approach, w + 2 * clr, w, bite, (zl - cav["z_bot"]) if axis_R[2, 2] > 0.9 else float("nan"), score, notes, needs,
                         wall_thickness_m=wall_t, rim_above_support_m=float((origin + axis_R @ np.r_[c, cav["z_top"]])[2] - z_support), clearance_inside_m=clear_in,
                         inner_jaw="toward the opening's middle", tip_moment_Nm=moment, azimuth_deg=round(math.degrees(th)) % 360))
    return _one_per_direction(out, key="close", bins=12, half_turn=False, keep=12)


# ------------------------------------------------------------------ 5 edge grasp
def edge(points, z_support, support_mask, mask_lo, mask_res, com=None, mass=0.0, n_head=24, max_slide=0.12):
    """support_mask: 2-D bool grid of the support's top (True = support), cell (i, j) at mask_lo + (i, j) * mask_res.
    For each outward direction a: how far the thing overhangs the edge (or how far it is from it), its thickness there."""
    P = np.asarray(points, float)
    com = P.mean(0) if com is None else np.asarray(com, float)
    xy0 = P[:, :2].mean(0)
    h = float(P[:, 2].max() - z_support)
    pw, pl, og = DEX1["pad_w"], DEX1["pad_l"], DEX1["open_gap"]
    nx, ny = support_mask.shape

    def on(p):
        i, j = np.round((np.asarray(p) - mask_lo) / mask_res).astype(int)
        return 0 <= i < nx and 0 <= j < ny and bool(support_mask[i, j])
    out = []
    for k in range(n_head):
        phi = 2 * math.pi * k / n_head
        a = np.array([math.cos(phi), math.sin(phi)]); n = np.array([-a[1], a[0]])
        pa = (P[:, :2] - xy0) @ a; pn = (P[:, :2] - xy0) @ n
        W = np.abs(pn) <= pw / 2
        if W.sum() < 3:
            continue
        s_th = float(pa[W].max())
        s_edge = None
        for sv in np.arange(0.0, 1.5, 0.005):
            if not any(on(xy0 + a * sv + n * dn) for dn in (-pw / 2, 0.0, pw / 2)):
                s_edge = sv; break
        if s_edge is None:
            continue
        over = s_th - s_edge
        need = 0.015
        slide = max(0.0, need - over + 0.003)
        if slide > max_slide:
            continue
        outer = W & (pa >= s_th - pl)
        zb, zt = float(P[outer, 2].min()), float(P[outer, 2].max())
        t = zt - zb
        if t > og - 0.001:
            continue
        bite = min(pl, max(over, 0.0) + slide)
        grip = xy0 + a * (s_th + slide - bite / 2)
        lever = float(np.linalg.norm((com[:2] + a * slide) - grip))
        moment = mass * G * lever
        cap6 = DEX1["squeeze_n"] * bite                   # the pad pair as a clamp: squeeze x pad length on the thing (as rim_pinch)
        v = "yes" if (over >= need or (s_edge - s_th) <= 0.03) and t <= og - 2 * CLEAR else "marginal"
        notes = []
        if over >= need:
            notes.append(f"overhangs the edge by {100 * over:.1f} cm: lower jaw straight under it")
        elif over > 0:
            notes.append(f"overhangs by {100 * over:.1f} cm only: slide it {100 * slide:.1f} cm out first")
        else:
            notes.append(f"{100 * -over:.1f} cm from the edge: slide it {100 * slide:.1f} cm out first" + ("" if -over <= 0.03 else " (more than 3 cm: long slide)"))
        notes.append(f"{100 * t:.1f} cm thick at the edge")
        if moment > cap6:
            notes.append(f"held at its edge the weight turns it {moment:.2f} N m (pads resist about {cap6:.2f} N m at 6 N): it will swing down to hang from the grip, or use two hands")
        needs = ["edge grasp: gripper turned so the jaws close vertically, fingers horizontal, lower jaw under the edge (new skill)"]
        if slide > 0:
            needs.append("slide to the edge: fingertips pressed on the thing, dragged outward (new skill)")
        score = slide + 0.2 * t + (0.05 if v == "marginal" else 0.0)
        out.append(_cand("edge", v, np.r_[grip, (zb + zt) / 2], [0, 0, 1], np.r_[-a, 0.0], t + 0.016, t, bite, zb - z_support, score, notes, needs,
                         overhang_m=over, edge_distance_m=max(0.0, -over), slide_m=slide, outward_deg=round(math.degrees(phi)) % 360, tip_moment_Nm=moment,
                         edge_point=[round(float(v_), 4) for v_ in (xy0 + a * s_edge)], height_m=h))
    return _one_per_direction(out, key="approach", bins=12, half_turn=False, keep=12)


# ------------------------------------------------------------------ reading the table
def load(path=os.path.join(HERE, "grasps_v2.json")):
    return json.load(open(path, encoding="utf-8"))["objects"]


ORDER = ("top_down", "side", "surface_pinch", "rim_pinch", "edge")


def candidates(table, name, type_):
    return table[name]["grasps"].get(type_, [])


def best(table, name, type_=None):
    """Best candidate: 'yes' before 'marginal', then in the order top_down, side, surface_pinch, rim_pinch, edge."""
    e = table[name]["grasps"]
    for verdict in ("yes", "marginal"):
        for t in ((type_,) if type_ else ORDER):
            for c in e.get(t, []):
                if c["verdict"] == verdict:
                    return c
    return None


def to_world(p):
    p = np.asarray(p, float).copy(); p[:2] -= START
    return p
