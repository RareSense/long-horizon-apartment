"""Where can a two-jaw gripper take a thing from above? Found from the thing's own collision shape (points on its
surface, world frame), for any object: no per-object rules.

The gripper comes straight down with the jaws open (gap `open_gap`), the two pads (pad_w wide, pad_h high) on either
side of a section of the object, and closes along a horizontal direction. A grasp is a section where
  - everything of the object above the pads' lower edge, within the pads' width along the section, fits between the
    open jaws with clearance (so the pads can come down past it);
  - there is something between the pads at pad height (at least `min_bite` of the pad height is covered);
  - the pads' lower edge stays `floor_clear` above the surface the object lies on.
Among these the narrowest, nearest the object's middle, wins (a narrow waist, a strap, a rim, a heel).

find(points, z_support) -> list of candidates sorted best first:
  dict(point (3,): middle between the pads, close (3,): unit closing direction, width, z (pad middle height),
       top (highest point of the object in the section), score)"""
from __future__ import annotations

import numpy as np

PAD_W, PAD_H = 0.029, 0.029          # Dex1 pad (along the section, up-down)
OPEN_GAP = 0.079                     # between the pad faces, fully open


def find(points, z_support, open_gap=OPEN_GAP, clearance=0.0045, pad_w=PAD_W, pad_h=PAD_H, floor_clear=0.006, min_bite=0.008,
         n_dir=18, step=0.01, max_palm=0.062):
    """max_palm: the palm is this far above the pad middle; the object's top in the section may not be higher."""
    P = np.asarray(points, float)
    c0 = P[:, :2].mean(0)
    lo_z, hi_z = P[:, 2].min(), P[:, 2].max()
    out = []
    wmax = open_gap - 2 * clearance
    for k in range(n_dir):
        a = np.pi * k / n_dir
        u = np.array([np.cos(a), np.sin(a)]); v = np.array([-u[1], u[0]])        # u: closing direction, v: along the section
        pu = P[:, :2] @ u; pv = P[:, :2] @ v
        for s in np.arange(pv.min() + pad_w / 2 - 0.004, pv.max() - pad_w / 2 + 0.004 + 1e-9, step):
            win = np.abs(pv - s) <= pad_w / 2 + 0.003                            # what the pads' width covers (+3 mm)
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
                # the jaws' outer bodies (about 1.5 cm thick beyond each pad face) must not come down on other parts of
                # the object: nothing of it above the pads' lower edge within the open jaws' sweep outside the section
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


def body_points(m, d, body_id, per_face=1):
    """Surface points (world) of a body's colliding shapes from the controller's model: mesh vertices (+ face centres),
    box corners and edge points, cylinder / sphere / capsule rings."""
    import mujoco
    P = []
    for g in range(m.ngeom):
        if int(m.geom_bodyid[g]) != body_id or (m.geom_contype[g] == 0 and m.geom_conaffinity[g] == 0):
            continue
        R = d.geom_xmat[g].reshape(3, 3); c = d.geom_xpos[g]; t = int(m.geom_type[g]); sz = m.geom_size[g]
        if t == int(mujoco.mjtGeom.mjGEOM_MESH):
            mid = int(m.geom_dataid[g]); a = int(m.mesh_vertadr[mid]); n = int(m.mesh_vertnum[mid])
            V = m.mesh_vert[a:a + n]
            fa = int(m.mesh_faceadr[mid]); fn = int(m.mesh_facenum[mid])
            F = m.mesh_face[fa:fa + fn]
            L = [V, V[F].mean(1)] + [(V[F[:, i]] + V[F[:, (i + 1) % 3]]) / 2 for i in range(3)]
            Q = np.vstack(L)
        elif t == int(mujoco.mjtGeom.mjGEOM_BOX):
            g1 = np.linspace(-1, 1, 7)
            Q = np.array([[x, y, z] for x in g1 for y in g1 for z in g1 if max(abs(x), abs(y), abs(z)) == 1.0]) * sz
        else:
            r = sz[0]; h = sz[1] if t in (int(mujoco.mjtGeom.mjGEOM_CYLINDER), int(mujoco.mjtGeom.mjGEOM_CAPSULE)) else 0.0
            th = np.linspace(0, 2 * np.pi, 24, endpoint=False)
            if t == int(mujoco.mjtGeom.mjGEOM_SPHERE):
                ph = np.linspace(-np.pi / 2, np.pi / 2, 9)
                Q = np.array([[r * np.cos(p_) * np.cos(a_), r * np.cos(p_) * np.sin(a_), r * np.sin(p_)] for p_ in ph for a_ in th])
            else:
                Q = np.array([[r * np.cos(a_), r * np.sin(a_), z] for z in np.linspace(-h, h, 7) for a_ in th] + [[0, 0, -h], [0, 0, h]])
        P.append(c + Q @ R.T)
    return np.vstack(P) if P else np.zeros((0, 3))
