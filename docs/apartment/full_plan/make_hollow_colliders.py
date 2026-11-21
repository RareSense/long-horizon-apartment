r"""Hollow colliders for the open containers of Apartment 1122 (cups, glasses, mugs, bowls, pitcher, canister ...).

    py -3.12 C:\Users\raresense\sim_home\apartment\full_plan\make_hollow_colliders.py

WHY: every loose dish in the pack collides as ONE solid convex hull (environment.xml: object_NNNN_collision_00, a hull of
the outside). A jaw cannot go inside a cup, so a rim pinch is impossible in simulation. This script builds, from the
VISUAL mesh (which is hollow), a small set of boxes per container: N wall slabs round the opening (tilted to follow a
tapered or sloped wall, one or two segments high), a floor (one square box, or 4 bars turned 45 deg = an octagon for a
base over 6 cm across), and one box per handle / spout. Inside is left clear down to the cavity floor. Walls are at
least 3 mm thick (the mesh's own thickness, less the polygon's corner allowance). Plates, lids and the two bowls that
are filled to 1.2 cm below the rim (open less than 1.5 cm deep) stay solid, as do lidded / closed containers.

Reads (never writes) D:\apartment_real\mujoco\unzipped\environment.xml + scene_spec.json. Writes beside this script:
  hollow_colliders.json   per body: geoms to remove, box geoms to add (BODY frame, MJCF size = half sizes, quat w x y z),
                          the body's inertial (unchanged: the new geoms have mass 0, the explicit <inertial> stays), QC
  hollow_colliders_qc.png section and top view of every shell over the visual mesh points
For OUR merged model only (E:\urc_home\src\urc\tasks\home\apartment.py builds it from the pack's XML; the pack is not
changed). apply_to_body(el, entry) below does the swap on the body's ElementTree element. BY GEOMETRY, NOT VERIFIED
in simulation: contact behaviour of the shells (resting, sliding, a jaw inside) has not been run."""
from __future__ import annotations

import math
import os
import xml.etree.ElementTree as ET

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "D:/apartment_real/mujoco/unzipped"
MIN_WALL = 0.003            # m, thinnest wall slab
MIN_DEPTH = 0.015           # m, open less deep than this: not a container (plates, lids, trays stay solid)
INCLUDE_CLS = ("dish", "container", "kitchenware", "cookware")   # bags, baskets (the toy basket is already 5 pieces), plants, the TV: not containers to pinch


# ------------------------------------------------------------------ applying it (pure Python, for the room builder)
def apply_to_body(el, entry):
    """Swap the collider of one pack body in OUR merged MJCF: `el` is the <body name="object_NNNN_body"> ElementTree
    element, `entry` = hollow_colliders.json["bodies"][display name]. Removes the pack's collision geoms, adds the
    boxes (mass 0: the body's explicit <inertial> keeps mass and inertia). Call it before the builder sets contype /
    conaffinity of loose bodies (it then treats the boxes like any other collision geom)."""
    for g in list(el.findall("geom")):
        if g.get("name") in entry["remove_geoms"]:
            el.remove(g)
    for g in entry["geoms"]:
        ET.SubElement(el, "geom", name=g["name"], type="box", size=" ".join(f"{v:.5f}" for v in g["size"]),
                      pos=" ".join(f"{v:.5f}" for v in g["pos"]), quat=" ".join(f"{v:.7f}" for v in g["quat"]),
                      mass="0", group="3", rgba="0 0 0 0", contype="1", conaffinity="1", condim=str(entry.get("condim", 3)),
                      friction=" ".join(str(v) for v in entry.get("friction", [0.6, 0, 0])))
    return el


# ------------------------------------------------------------------ geometry helpers (numpy)
def sample_surface(V, F, spacing=0.002, cap=60000, seed=0):
    """Points on a triangle mesh (vertices + random points about `spacing` apart)."""
    rng = np.random.default_rng(seed)
    A = V[F]; ar = 0.5 * np.linalg.norm(np.cross(A[:, 1] - A[:, 0], A[:, 2] - A[:, 0]), axis=1)
    n = np.ceil(ar / spacing ** 2 * 2).astype(int)
    if n.sum() > cap:
        n = np.ceil(n * cap / n.sum()).astype(int)
    idx = np.repeat(np.arange(len(F)), n)
    u = rng.random((len(idx), 2)); s = u.sum(1) > 1; u[s] = 1 - u[s]
    T = A[idx]
    return np.vstack([V, T[:, 0] + u[:, :1] * (T[:, 1] - T[:, 0]) + u[:, 1:] * (T[:, 2] - T[:, 0])])


def rz(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def mat2quat(R):
    """Rotation matrix -> quaternion w x y z."""
    t = np.trace(R)
    if t > 0:
        s = math.sqrt(t + 1.0) * 2; w = 0.25 * s; x = (R[2, 1] - R[1, 2]) / s; y = (R[0, 2] - R[2, 0]) / s; z = (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = math.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2; w = (R[2, 1] - R[1, 2]) / s; x = 0.25 * s; y = (R[0, 1] + R[1, 0]) / s; z = (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = math.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2; w = (R[0, 2] - R[2, 0]) / s; x = (R[0, 1] + R[1, 0]) / s; y = 0.25 * s; z = (R[1, 2] + R[2, 1]) / s
    else:
        s = math.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2; w = (R[1, 0] - R[0, 1]) / s; x = (R[0, 2] + R[2, 0]) / s; y = (R[1, 2] + R[2, 1]) / s; z = 0.25 * s
    q = np.array([w, x, y, z]); q /= np.linalg.norm(q)
    return q if q[0] >= 0 else -q


def box_sdf(P, c, R, h):
    """Signed distance of points P (n, 3) to a box (centre c, rotation R (columns = box axes), half sizes h)."""
    q = np.abs((P - c) @ R) - h
    out = np.linalg.norm(np.maximum(q, 0.0), axis=1)
    ins = np.minimum(np.max(q, axis=1), 0.0)
    return out + ins


def axis_frames(P):
    """Candidate container axes: up, down and (for a thing lying down) both ways along its long horizontal axis."""
    out = [np.eye(3), np.diag([1.0, -1.0, -1.0])]
    ext = np.ptp(P, axis=0)
    Q = P[:, :2] - P[:, :2].mean(0)
    w, v = np.linalg.eigh(Q.T @ Q)
    h = np.r_[v[:, -1], 0.0]
    if np.ptp(P[:, :2] @ v[:, -1]) > 1.3 * ext[2]:
        for sg in (1.0, -1.0):
            z_ = sg * h; x_ = np.array([0.0, 0.0, 1.0]); y_ = np.cross(z_, x_)
            out.append(np.c_[x_, y_, z_])
    return out


def kasa(xy):
    """Least-squares circle through points (centre, radius)."""
    A = np.c_[2 * xy, np.ones(len(xy))]; b = (xy ** 2).sum(1)
    s, *_ = np.linalg.lstsq(A, b, rcond=None)
    c = s[:2]; r = math.sqrt(max(s[2] + c @ c, 1e-12))
    return c, r


def cavity(Q, nsec=24, min_depth=None):
    """Q: points in a candidate axis frame (z = the opening's direction). Returns the open cavity, or None."""
    z_top, z_bot = Q[:, 2].max(), Q[:, 2].min()
    top = Q[Q[:, 2] > z_top - 0.006]
    c = (top[:, :2].min(0) + top[:, :2].max(0)) / 2
    for _ in range(2):                                       # inner rim: nearest top point per sector -> circle fit
        d = top[:, :2] - c; ang = np.arctan2(d[:, 1], d[:, 0]); r = np.linalg.norm(d, axis=1)
        k = ((ang + math.pi) / (2 * math.pi) * nsec).astype(int) % nsec
        rim = np.array([top[k == i][np.argmin(r[k == i]), :2] for i in range(nsec) if (k == i).any()])
        if len(rim) < 8:
            return None
        c, r_rim = kasa(rim)
    rr = np.linalg.norm(Q[:, :2] - c, axis=1)
    col = rr < max(0.5 * r_rim, 0.006)
    if not col.any():
        return None
    z_floor = float(Q[col, 2].max())
    depth = z_top - z_floor
    if depth < (MIN_DEPTH if min_depth is None else min_depth) or r_rim < 0.015:
        return None
    return dict(c=c, r_rim_in=float(r_rim), z_top=float(z_top), z_bot=float(z_bot), z_floor=z_floor, depth=float(depth))


def profile(Q, cav, nsec=16, dz=0.004):
    """Inner and outer radius of the wall against height (median over sectors: a handle does not count)."""
    c = cav["c"]; d = Q[:, :2] - c; r = np.linalg.norm(d, axis=1); ang = np.arctan2(d[:, 1], d[:, 0])
    k = ((ang + math.pi) / (2 * math.pi) * nsec).astype(int) % nsec
    rows = []
    for z0 in np.arange(cav["z_bot"], cav["z_top"] + 1e-9, dz):
        sel = (Q[:, 2] >= z0) & (Q[:, 2] < z0 + dz)
        if sel.sum() < nsec:
            continue
        above = z0 > cav["z_floor"] + 0.002
        ins, outs = [], []
        for i in range(nsec):
            s = sel & (k == i)
            if not s.any():
                continue
            outs.append(r[s].max())
            if above:
                w = s & (r > 0.4 * cav["r_rim_in"])
                if w.any():
                    ins.append(r[w].min())
        rows.append((z0 + dz / 2, float(np.median(ins)) if ins else np.nan, float(np.median(outs))))
    return np.array(rows)


def fit_segments(z, r, max_res=0.003):
    """One straight line r(z) or two (split where the larger residual is least)."""
    def line(zz, rr):
        A = np.c_[zz, np.ones(len(zz))]; s, *_ = np.linalg.lstsq(A, rr, rcond=None)
        return s, float(np.abs(A @ s - rr).max())
    s, res = line(z, r)
    if res <= max_res or len(z) < 8:
        return [(z[0], z[-1], s)]
    best = None
    for i in range(3, len(z) - 3):
        s1, e1 = line(z[:i + 1], r[:i + 1]); s2, e2 = line(z[i:], r[i:])
        if best is None or max(e1, e2) < best[0]:
            best = (max(e1, e2), i, s1, s2)
    _, i, s1, s2 = best
    return [(z[0], z[i], s1), (z[i], z[-1], s2)]


def build_shell(Q, cav, prof):
    """Boxes in the axis frame: list of (centre (3,), R (3x3, columns = box axes), half sizes (3,), role)."""
    boxes = []
    zp, rin, rout = prof[:, 0], prof[:, 1], prof[:, 2]
    wall = ~np.isnan(rin)
    zw, rw, ow = zp[wall], rin[wall], rout[wall]
    r_out_max = float(np.nanmax(rout))
    N = 8 if r_out_max <= 0.05 else (10 if r_out_max <= 0.08 else 12)
    cosN, tanN = math.cos(math.pi / N), math.tan(math.pi / N)
    base_h = cav["z_floor"] - cav["z_bot"]
    thin_bottom = base_h <= 0.015
    segs = fit_segments(zw, rw)
    t_h_all = ow - rw
    info = dict(n_wall_sectors=N, wall_segments=len(segs), filled=not thin_bottom)
    wall_t = []
    for si, (za, zb, s) in enumerate(segs):
        if si == 0:
            za = cav["z_bot"] if thin_bottom else cav["z_floor"] - 0.003
        if si == len(segs) - 1:
            zb = cav["z_top"]
        ra, rb = s[0] * za + s[1], s[0] * zb + s[1]
        sel = (zw >= za - 1e-9) & (zw <= zb + 1e-9)
        t_h = float(np.median(t_h_all[sel])) if sel.any() else MIN_WALL
        r_mid = (ra + rb) / 2
        t_box = max((r_mid + t_h) * (1 + cosN) / 2 - r_mid, MIN_WALL)  # outer face halfway between the inscribed and the circumscribed polygon of the outer surface
        L = math.hypot(rb - ra, zb - za)
        sdir = np.array([rb - ra, 0.0, zb - za]) / L
        n = np.array([sdir[2], 0.0, -sdir[0]])
        t_n = max(t_box * abs(sdir[2]), MIN_WALL)
        wall_t.append(t_n)
        Lt = 2 * (r_mid + t_box) * tanN
        for k in range(N):
            th = 2 * math.pi * k / N
            Rk = rz(th)
            cen_l = np.array([r_mid, 0.0, (za + zb) / 2]) + n * t_n / 2
            Rl = np.c_[n, [0.0, 1.0, 0.0], sdir]
            boxes.append((np.r_[cav["c"], 0.0] + Rk @ cen_l, Rk @ Rl, np.array([t_n / 2, Lt / 2, L / 2 + 0.0015]), "wall"))
    info["wall_thickness_mm"] = [round(1000 * t, 1) for t in wall_t]
    info["wall_thickness_from_mesh_mm"] = round(1000 * float(np.median(t_h_all)), 1)
    info["inner_radius_top_cm"] = round(100 * float(segs[-1][2][0] * cav["z_top"] + segs[-1][2][1]), 2)
    info["inner_radius_bottom_cm"] = round(100 * float(rw[0]), 2)
    # floor / solid base: octagon layers (one box when small), inscribed in the outer surface of each layer
    zs = [cav["z_bot"], cav["z_floor"]]
    rb_lo = float(np.min(rout[(zp >= cav["z_bot"]) & (zp <= cav["z_floor"] + 0.004)])) if ((zp >= cav["z_bot"]) & (zp <= cav["z_floor"] + 0.004)).any() else float(rout[0])
    if not thin_bottom:
        r_top_base = float(np.median(rout[(zp > cav["z_floor"] - 0.02) & (zp <= cav["z_floor"])])) if ((zp > cav["z_floor"] - 0.02) & (zp <= cav["z_floor"])).any() else rb_lo
        if r_top_base - rb_lo > 0.01:
            zs = [cav["z_bot"], (cav["z_bot"] + cav["z_floor"]) / 2, cav["z_floor"]]
    for z0, z1 in zip(zs[:-1], zs[1:]):
        sel = (zp >= z0 - 0.002) & (zp <= z1 + 0.002)
        R_ = float(np.min(rout[sel])) if sel.any() else rb_lo
        if thin_bottom:
            R_ = min(R_, float(rw[0]) + t_h_all[0] if len(rw) else R_)
        top = max(z1, z0 + MIN_WALL)
        hz = (top - z0) / 2
        if R_ < 0.06:                                          # one square inscribed in the base (the wall slabs close the edge gaps)
            a = R_ / math.sqrt(2)
            boxes.append((np.r_[cav["c"], z0 + hz], np.eye(3), np.array([a, a, hz]), "floor"))
        else:                                                  # union of 4 bars turned 45 deg = an octagon inscribed in the base
            a = R_ * math.cos(math.pi / 8)
            for th in (0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4):
                boxes.append((np.r_[cav["c"], z0 + hz], rz(th), np.array([a, a * math.tan(math.pi / 8), hz]), "floor"))
    info["floor_layers"] = len(zs) - 1
    # handles and spouts: what sticks out beyond the outer wall, one box per cluster (at most two)
    d = Q[:, :2] - cav["c"]; r = np.linalg.norm(d, axis=1); ang = np.arctan2(d[:, 1], d[:, 0])
    r_out_z = np.interp(Q[:, 2], zp, rout)
    hp = r > r_out_z + 0.006
    info["handles"] = 0
    if hp.sum() >= 30:
        a_ = np.sort(ang[hp]); gaps = np.diff(np.r_[a_, a_[0] + 2 * math.pi])
        cut = np.where(gaps > math.radians(25))[0]
        starts = (cut + 1) % len(a_) if len(cut) else [0]
        clusters = []
        for i, st in enumerate(starts):
            lo_a = a_[st]; hi_a = a_[cut[(i + 1) % len(cut)]] if len(cut) else a_[st - 1] + 2 * math.pi
            span = (hi_a - lo_a) % (2 * math.pi)
            sel = hp & (((ang - lo_a) % (2 * math.pi)) <= span + 1e-9)
            if sel.sum() >= 30:
                clusters.append(sel)
        for sel in sorted(clusters, key=lambda s_: -s_.sum())[:2]:
            mid = math.atan2(np.sin(ang[sel]).mean(), np.cos(ang[sel]).mean())
            Rk = rz(mid)
            L_ = (Q[sel] - np.r_[cav["c"], 0.0]) @ Rk
            r0 = float(np.min(r_out_z[sel])) * math.cos(math.pi / N) - 0.002
            lo_, hi_ = L_.min(0), L_.max(0); lo_[0] = min(lo_[0], r0)
            cen = np.r_[cav["c"], 0.0] + Rk @ ((lo_ + hi_) / 2)
            boxes.append((cen, Rk, np.maximum((hi_ - lo_) / 2, MIN_WALL / 2), "handle"))
            info["handles"] += 1
    return boxes, info


def qc(Q, cav, prof, boxes):
    """Inside clear? Visual surface covered? (axis frame)"""
    zp, rin = prof[:, 0], prof[:, 1]
    pts = []
    for z in np.arange(cav["z_floor"] + 0.004, cav["z_top"] - 0.001, 0.003):
        ri = np.interp(z, zp[~np.isnan(rin)], rin[~np.isnan(rin)]) - 0.0025
        for rr in np.arange(0.0, max(ri, 0.0) + 1e-9, 0.003):
            for th in np.linspace(0, 2 * math.pi, 24, endpoint=False):
                pts.append([cav["c"][0] + rr * math.cos(th), cav["c"][1] + rr * math.sin(th), z])
    pts = np.array(pts) if pts else np.zeros((0, 3))
    sd = np.min([box_sdf(pts, c, R, h) for c, R, h, _ in boxes], axis=0) if len(pts) else np.zeros(0)
    vs = np.min([box_sdf(Q, c, R, h) for c, R, h, _ in boxes], axis=0)
    return dict(cavity_probe_points=int(len(pts)), cavity_points_inside_shell=int((sd < -0.0005).sum()),
                visual_points_within_3mm_of_shell_pct=round(100.0 * float(np.mean(vs <= 0.003)), 1),
                visual_points_over_6mm_from_shell_pct=round(100.0 * float(np.mean(vs > 0.006)), 1))


# ------------------------------------------------------------------ main (needs mujoco)
def main():
    import json, time
    import mujoco
    T0 = time.time()
    spec = json.load(open(SRC + "/scene_spec.json", encoding="utf-8"))
    m = mujoco.MjModel.from_xml_path(SRC + "/environment.xml"); d = mujoco.MjData(m); mujoco.mj_forward(m, d)
    xml_bodies = {el.get("name"): el for el in ET.parse(SRC + "/environment.xml").getroot().find("worldbody") if el.tag == "body"}
    out = {}; skipped = {}; figs = []; CHECK = []
    for o in spec["objects"]:
        if (o.get("body") or {}).get("motion") != "free" or o["semantic_class"] not in INCLUDE_CLS:
            continue
        bid = m.body(o["id"] + "_body").id
        P = []
        for g in range(m.ngeom):
            if m.geom_bodyid[g] != bid or m.geom_type[g] != mujoco.mjtGeom.mjGEOM_MESH or m.geom_contype[g] or m.geom_conaffinity[g]:
                continue
            mid = int(m.geom_dataid[g]); a = int(m.mesh_vertadr[mid]); n = int(m.mesh_vertnum[mid])
            V = m.mesh_vert[a:a + n].astype(float) @ d.geom_xmat[g].reshape(3, 3).T + d.geom_xpos[g]
            fa = int(m.mesh_faceadr[mid]); fn = int(m.mesh_facenum[mid])
            P.append(sample_surface(V, m.mesh_face[fa:fa + fn]))
        if not P:
            continue
        P = np.vstack(P)
        o_ = P.mean(0)
        best = None
        for Rax in axis_frames(P):
            Q = (P - o_) @ Rax
            cv = cavity(Q)
            if cv is not None and (best is None or cv["depth"] > best[1]["depth"]):
                best = (Rax, cv, Q)
        if best is None:
            sh = [cavity((P - o_) @ Rax, min_depth=0.006) for Rax in axis_frames(P)]      # why not: a shallow opening, or none?
            sh = max((c_ for c_ in sh if c_ is not None), key=lambda c_: c_["depth"], default=None)
            if sh is not None:
                skipped[o["name"]] = (f"open only {100 * sh['depth']:.1f} cm deep (rim inner radius {100 * sh['r_rim_in']:.1f} cm, {100 * np.ptp(P[:, 2]):.1f} cm high): "
                                      + ("plate / lid: " if np.ptp(P[:, 2]) < 0.03 else "filled to near the rim (contents in the mesh): ") + "kept solid")
            elif o["semantic_class"] == "dish" or "cup" in o["name"] or "bowl" in o["name"]:
                skipped[o["name"]] = "no opening at the top in the visual mesh (closed or lidded, or stored upside down / packed): kept solid"
            continue
        Rax, cv, Q = best
        if np.ptp(P[:, 2]) < 0.03 and np.ptp(P[:, :2], axis=0).max() > 0.15:
            skipped[o["name"]] = f"plate-like ({100 * np.ptp(P[:, 2]):.1f} cm high, open {100 * cv['depth']:.1f} cm deep): kept solid"
            continue
        prof = profile(Q, cv)
        boxes, info = build_shell(Q, cv, prof)
        q_ = qc(Q, cv, prof, boxes)
        # to the BODY frame (the XML body frame = the compiled body frame at the start pose)
        bp, bR = d.xpos[bid].copy(), d.xmat[bid].reshape(3, 3).copy()
        geoms = []
        for i, (c, R, h, role) in enumerate(boxes):
            cw = o_ + Rax @ c; Rw = Rax @ R
            cb = bR.T @ (cw - bp); Rb = bR.T @ Rw
            geoms.append(dict(name=f"{o['id']}_hollow_{role[0]}{i:02d}", role=role, size=[round(float(v), 5) for v in h], pos=[round(float(v), 5) for v in cb],
                              quat=[round(float(v), 7) for v in mat2quat(Rb)]))
        el = xml_bodies[o["id"] + "_body"]
        inert = el.find("inertial")
        col = [g.get("name") for g in el.findall("geom") if "_collision_" in g.get("name", "")]
        cg = next(g for g in el.findall("geom") if "_collision_" in g.get("name", ""))
        up = Rax[:, 2]
        orient = "upright" if up[2] > 0.9 else ("upside down" if up[2] < -0.9 else "lying on its side")
        out[o["name"]] = dict(
            id=o["id"], body=o["id"] + "_body", cls=o["semantic_class"], mass_kg=float(o["body"]["mass"]), opening=orient,
            remove_geoms=col, condim=int(cg.get("condim", 3)), friction=[float(v) for v in cg.get("friction", "0.6 0 0").split()],
            inertial_unchanged=dict(mass=float(inert.get("mass")), pos=inert.get("pos"), diaginertia=inert.get("diaginertia")) if inert is not None else None,
            n_geoms=len(geoms), geoms=geoms,
            geometry=dict(depth_open_cm=round(100 * cv["depth"], 1), rim_inner_radius_cm=round(100 * cv["r_rim_in"], 2), height_cm=round(100 * (cv["z_top"] - cv["z_bot"]), 1),
                          floor_or_contents_above_bottom_cm=round(100 * (cv["z_floor"] - cv["z_bot"]), 1), **info),
            qc=q_, basis="by geometry, not verified")
        figs.append((o["name"], Q, cv, boxes, orient))
        CHECK.append((o["name"], bp, d.xquat[bid].copy(), geoms, P, o_, Rax, cv, prof))
        print(f"{o['name']:26s} {orient:17s} depth {100 * cv['depth']:5.1f} cm  geoms {len(geoms):2d} (walls {info['n_wall_sectors']}x{info['wall_segments']}, floor layers {info['floor_layers']}, handles {info['handles']})"
              f"  wall {info['wall_thickness_mm']} mm  cavity pts inside {q_['cavity_points_inside_shell']}/{q_['cavity_probe_points']}  vis within 3 mm {q_['visual_points_within_3mm_of_shell_pct']}%", flush=True)
    # independent check through MuJoCo itself: the boxes exactly as written (body pose + pos/quat/size) compiled, then
    # the visual surface and the cavity tested against MuJoCo's own geom poses (catches a wrong frame or quaternion order)
    sp = mujoco.MjSpec()
    for name, bp, bq, geoms, P, o_, Rax, cv, prof in CHECK:
        b = sp.worldbody.add_body(name=name, pos=bp.tolist(), quat=bq.tolist())
        for g in geoms:
            b.add_geom(name=g["name"], type=mujoco.mjtGeom.mjGEOM_BOX, size=g["size"], pos=g["pos"], quat=g["quat"])
    mc = sp.compile(); dc = mujoco.MjData(mc); mujoco.mj_forward(mc, dc)
    for name, bp, bq, geoms, P, o_, Rax, cv, prof in CHECK:
        ids = [mc.geom(g["name"]).id for g in geoms]
        sd = np.min([box_sdf(P, dc.geom_xpos[i], dc.geom_xmat[i].reshape(3, 3), mc.geom_size[i]) for i in ids], axis=0)
        zp, rin = prof[:, 0], prof[:, 1]; ok = ~np.isnan(rin)
        cav_pts = []
        for z in np.arange(cv["z_floor"] + 0.004, cv["z_top"] - 0.001, 0.004):
            ri = np.interp(z, zp[ok], rin[ok]) - 0.0025
            for rr in np.arange(0.0, max(ri, 0.0) + 1e-9, 0.004):
                for th in np.linspace(0, 2 * math.pi, 16, endpoint=False):
                    cav_pts.append(o_ + Rax @ np.array([cv["c"][0] + rr * math.cos(th), cv["c"][1] + rr * math.sin(th), z]))
        cav_pts = np.array(cav_pts)
        sc = np.min([box_sdf(cav_pts, dc.geom_xpos[i], dc.geom_xmat[i].reshape(3, 3), mc.geom_size[i]) for i in ids], axis=0)
        out[name]["qc"]["mujoco_check"] = dict(visual_points_within_3mm_pct=round(100.0 * float(np.mean(sd <= 0.003)), 1),
                                               cavity_points_inside_shell=int((sc < -0.0005).sum()), cavity_points=int(len(cav_pts)))
        if name.startswith("r66i"):
            out[name]["note"] = "stored upside down in the open dishwasher's top rack: in place, frozen in today's room; listed for completeness"
    res = dict(
        title="Hollow colliders for the open containers of Apartment 1122 (OUR merged model only; the pack is not changed)",
        generator=os.path.abspath(__file__).replace("\\", "/"), basis="by geometry, not verified in simulation",
        how_to_apply="In the room builder, for each body listed: remove the geoms in remove_geoms (the pack's solid convex hull) and add the boxes "
                     "(MJCF: type box, size = half sizes, pos/quat in the BODY frame, quat w x y z, mass 0, group 3, invisible). The body's explicit "
                     "<inertial> stays, so mass and inertia are unchanged. Visual mesh unchanged. make_hollow_colliders.apply_to_body(el, entry) does it on "
                     "the ElementTree body element; run it before the builder sets contype/conaffinity of loose bodies.",
        why="The pack collides every dish as ONE solid convex hull (no inside): a jaw cannot enter a cup, so a rim pinch is impossible until the collider is hollow.",
        rules=dict(min_wall_m=MIN_WALL, min_open_depth_m=MIN_DEPTH, wall_sectors="8 (outer radius up to 5 cm), 10 (up to 8 cm), 12 (larger); 1 or 2 tilted segments high",
                   floor="1 square box (base radius under 6 cm) or 4 bars turned 45 deg (octagon); 2 layers when the solid base widens by over 1 cm",
                   handles="one box per handle / spout (at most 2)", outer_face="halfway between the inscribed and the circumscribed polygon of the outer surface (within about 1.5 mm of it), inner face on the inner surface (inside clear), walls at least 3 mm"),
        counts=dict(bodies=len(out), geoms_total=sum(v["n_geoms"] for v in out.values()), geoms_per_body={k: v["n_geoms"] for k, v in out.items()}),
        kept_solid=skipped, bodies=out)
    json.dump(res, open(os.path.join(HERE, "hollow_colliders.json"), "w", encoding="utf-8"), indent=1)
    # contact sheet: section through the axis (r, z) and top view at mid height
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(figs); cols = 4; rows_ = math.ceil(n / cols)
    fig, axs = plt.subplots(rows_, cols * 2, figsize=(cols * 2 * 2.6, rows_ * 2.7))
    axs = np.atleast_2d(axs)
    for i, (name, Q, cv, boxes, orient) in enumerate(figs):
        a1, a2 = axs[i // cols, (i % cols) * 2], axs[i // cols, (i % cols) * 2 + 1]
        c3 = np.r_[cv["c"], 0.0]
        sl = np.abs(Q[:, 1] - cv["c"][1]) < 0.002
        a1.scatter(Q[sl, 0] - cv["c"][0], Q[sl, 2], s=0.3, c="0.55")
        G = np.stack(np.meshgrid(np.linspace(Q[:, 0].min() - 0.01, Q[:, 0].max() + 0.01, 160), np.linspace(Q[:, 2].min() - 0.005, Q[:, 2].max() + 0.005, 120)), -1).reshape(-1, 2)
        P3 = np.c_[G[:, 0], np.full(len(G), cv["c"][1]), G[:, 1]]
        ins = np.min([box_sdf(P3, c, R, h) for c, R, h, _ in boxes], axis=0) <= 0
        a1.scatter(P3[ins, 0] - cv["c"][0], P3[ins, 2], s=0.4, c="tab:red", alpha=0.35)
        a1.set_title(f"{name}\n{orient}: section", fontsize=6); a1.set_aspect("equal"); a1.tick_params(labelsize=4)
        zm = (cv["z_floor"] + cv["z_top"]) / 2
        sl2 = np.abs(Q[:, 2] - zm) < 0.002
        a2.scatter(Q[sl2, 0], Q[sl2, 1], s=0.3, c="0.55")
        G2 = np.stack(np.meshgrid(np.linspace(Q[:, 0].min() - 0.01, Q[:, 0].max() + 0.01, 140), np.linspace(Q[:, 1].min() - 0.01, Q[:, 1].max() + 0.01, 140)), -1).reshape(-1, 2)
        P4 = np.c_[G2, np.full(len(G2), zm)]
        ins2 = np.min([box_sdf(P4, c, R, h) for c, R, h, _ in boxes], axis=0) <= 0
        a2.scatter(P4[ins2, 0], P4[ins2, 1], s=0.4, c="tab:red", alpha=0.35)
        a2.set_title("top view, mid height", fontsize=6); a2.set_aspect("equal"); a2.tick_params(labelsize=4)
    for j in range(n, rows_ * cols):
        axs[j // cols, (j % cols) * 2].axis("off"); axs[j // cols, (j % cols) * 2 + 1].axis("off")
    fig.suptitle("Hollow colliders (red = boxes) over the visual mesh (grey): by geometry, not verified", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "hollow_colliders_qc.png"), dpi=130)
    print(f"{len(out)} bodies, {res['counts']['geoms_total']} geoms; kept solid: {skipped}; {time.time() - T0:.0f} s")


if __name__ == "__main__":
    main()
