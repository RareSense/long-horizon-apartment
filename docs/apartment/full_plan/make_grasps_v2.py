r"""Grasp geometry v2 for every loose thing of Apartment 1122: candidate grasps of the Dex1 two-jaw gripper by type.

    py -3.12 C:\Users\raresense\sim_home\apartment\full_plan\make_grasps_v2.py

Reads (never writes) D:\apartment_real\mujoco\unzipped (environment.xml, scene_spec.json) and hollow_colliders.json
beside this script. Writes grasps_v2.json beside it (read it with grasp_types.load()). Pure geometry at the pack's
start poses: BY GEOMETRY, NOT VERIFIED in simulation. Scene frame (episode world = scene - (0.90, 0.45))."""
import json, math, os, sys, time
import numpy as np
import mujoco
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import grasp_types as GT
import make_hollow_colliders as HC

SRC = "D:/apartment_real/mujoco/unzipped"
NOT_SUPPORT = ("floor", "ceiling", "wall", "scenery", "rug", "skirting", "light_fixture", "curtain_rail", "duct", "curtain", "glass")


def main():
    T0 = time.time()
    spec = json.load(open(SRC + "/scene_spec.json", encoding="utf-8"))
    m = mujoco.MjModel.from_xml_path(SRC + "/environment.xml"); d = mujoco.MjData(m); mujoco.mj_forward(m, d)
    hollow = json.load(open(os.path.join(HERE, "hollow_colliders.json"), encoding="utf-8"))["bodies"]
    objs = {o["name"]: o for o in spec["objects"]}
    for o in objs.values():
        b = np.asarray(o["bounds_m"], float); o["_lo"], o["_hi"] = b[0], b[1]; o["_c"] = (b[0] + b[1]) / 2

    def geoms_of(oid, collide=True):
        out = []
        for g in range(m.ngeom):
            nm = m.geom(g).name
            if not nm.startswith(oid) or m.geom_type[g] != mujoco.mjtGeom.mjGEOM_MESH:
                continue
            if bool(m.geom_contype[g] or m.geom_conaffinity[g]) == collide:
                out.append(g)
        return out

    def tri(g):
        mid = int(m.geom_dataid[g]); a = int(m.mesh_vertadr[mid]); n = int(m.mesh_vertnum[mid])
        V = m.mesh_vert[a:a + n].astype(float) @ d.geom_xmat[g].reshape(3, 3).T + d.geom_xpos[g]
        fa = int(m.mesh_faceadr[mid]); fn = int(m.mesh_facenum[mid])
        return V, m.mesh_face[fa:fa + fn]

    def vef(g):
        """vertices + face centres + edge middles (the floor agent's body_points for a mesh)."""
        V, F = tri(g)
        return np.vstack([V, V[F].mean(1)] + [(V[F[:, i]] + V[F[:, (i + 1) % 3]]) / 2 for i in range(3)])

    def support_of(o):
        if o["_lo"][2] < 0.04:
            return "floor", 0.0
        best = None
        for q in objs.values():
            if q is o or q["semantic_class"] in NOT_SUPPORT:
                continue
            if np.all(o["_c"][:2] > q["_lo"][:2] - 0.02) and np.all(o["_c"][:2] < q["_hi"][:2] + 0.02):
                dz = o["_lo"][2] - q["_hi"][2]
                if -0.06 < dz < 0.04:
                    k = (0, abs(dz), q["name"])
                elif q["_lo"][2] - 0.02 < o["_lo"][2] < q["_hi"][2]:
                    k = (1, float(np.prod(q["_hi"] - q["_lo"])), q["name"])
                else:
                    continue
                if best is None or k[:2] < best[:2]:
                    best = k
        return (best[2] if best else "unknown"), None

    MASKS = {}

    def support_mask(sup, z):
        key = (sup, round(z, 2))
        if key not in MASKS:
            S = [HC.sample_surface(*tri(g), spacing=0.006, cap=200000) for g in geoms_of(objs[sup]["id"])] if sup in objs else []
            S = np.vstack(S) if S else np.zeros((0, 3))
            S = S[np.abs(S[:, 2] - z) <= 0.015]
            if len(S) < 10:
                MASKS[key] = None
            else:
                res = 0.01; lo = S[:, :2].min(0) - 0.05
                ij = np.round((S[:, :2] - lo) / res).astype(int)
                M = np.zeros(tuple(ij.max(0) + 6), bool); M[ij[:, 0], ij[:, 1]] = True
                M = ndimage.binary_closing(M, iterations=2)
                MASKS[key] = (M, lo, res)
        return MASKS[key]

    out = {}
    counts = {t: dict(yes=0, marginal=0) for t in GT.ORDER}
    for o in spec["objects"]:
        body = o.get("body") or {}
        if body.get("motion") != "free":
            continue
        bid = m.body(o["id"] + "_body").id
        mass = float(body.get("mass") or 0.0)
        cg = geoms_of(o["id"]); vg = geoms_of(o["id"], collide=False)
        Pc = np.vstack([vef(g) for g in cg]) if cg else np.zeros((0, 3))
        Pd = np.vstack([HC.sample_surface(*tri(g), spacing=0.003, cap=8000) for g in cg]) if cg else Pc
        Pv = np.vstack([HC.sample_surface(*tri(g), spacing=0.002, cap=40000) for g in vg]) if vg else Pd
        sup, _ = support_of(o)
        zs = max(0.0, float(Pc[:, 2].min())) if len(Pc) else float(o["_lo"][2])
        h = float(Pc[:, 2].max() - zs) if len(Pc) else 0.0
        com = d.xipos[bid].copy()
        e = dict(id=o["id"], body=o["id"] + "_body", cls=o["semantic_class"], mass_kg=mass, support=sup, z_support_m=round(zs, 4), height_m=round(h, 4),
                 hollow_collider=o["name"] in hollow, grasps={}, why_not={}, basis=GT.BASIS)
        if mass > 3.0 or not len(Pc):
            e["why_not"]["all"] = f"{mass:.1f} kg: furniture / too heavy, not searched"
            out[o["name"]] = e; continue
        g = e["grasps"]
        g["top_down"] = GT.top_down(Pc, zs, mass)
        if not g["top_down"]:
            e["why_not"]["top_down"] = "no section the open jaws (7.9 cm) can come straight down over"
        g["surface_pinch"] = GT.surface_pinch(Pc, zs, mass)
        if not g["surface_pinch"]:
            e["why_not"]["surface_pinch"] = (f"{100 * h:.1f} cm high: under 1 cm, nothing for the pads even with the fingertips on the support" if h < 0.010 else
                                            ("over 6 cm high: not a low thing" if h > 0.06 else "no section the open jaws can straddle at the support"))
        g["side"] = GT.side(Pd, zs, com, mass)
        if not g["side"]:
            e["why_not"]["side"] = ("too low for level fingers (pads need about 2 cm above the support)" if h < 0.03 else "no horizontal section under 7.9 cm the fingers and palm can reach")
        # rim pinch: the opening from the visual mesh (as the hollow collider was made)
        o_ = Pv.mean(0); cav = None
        for Rax in HC.axis_frames(Pv):
            cv = HC.cavity((Pv - o_) @ Rax, min_depth=0.008)
            if cv is not None and (cav is None or cv["depth"] > cav[1]["depth"]):
                cav = (Rax, cv)
        if cav is not None:
            e["opening"] = dict(depth_m=round(cav[1]["depth"], 4), rim_inner_radius_m=round(cav[1]["r_rim_in"], 4), axis=[round(float(v), 3) for v in cav[0][:, 2]])
            g["rim_pinch"] = GT.rim_pinch(Pv, zs, cav[1], cav[0], o_, mass, hollow=o["name"] in hollow)
            if not g["rim_pinch"]:
                e["why_not"]["rim_pinch"] = f"open {100 * cav[1]['depth']:.1f} cm deep but no wall section the part-open jaws fit round with the inner jaw clear"
        else:
            g["rim_pinch"] = []
            e["why_not"]["rim_pinch"] = "no opening (not a cup, glass, bowl or mug)"
        # edge grasp: flat things on furniture
        g["edge"] = []
        if sup != "floor" and h <= 0.08:
            M = support_mask(sup, zs)
            if M is not None:
                g["edge"] = GT.edge(Pd, zs, M[0], M[1], M[2], com, mass, max_slide=0.30)
                if not g["edge"]:
                    e["why_not"]["edge"] = "no edge of its support within a 30 cm slide, or too thick at the edge"
            else:
                e["why_not"]["edge"] = f"support {sup}: no top surface found at {zs:.2f} m"
        else:
            e["why_not"]["edge"] = "on the floor (no table edge)" if sup == "floor" else f"{100 * h:.0f} cm high: not a flat thing"
        for t in GT.ORDER:
            vs = {c["verdict"] for c in g.get(t, [])}
            if "yes" in vs:
                counts[t]["yes"] += 1
            elif "marginal" in vs:
                counts[t]["marginal"] += 1
        out[o["name"]] = e
    res = dict(title="Grasp geometry v2, Apartment 1122: candidate grasps of the Dex1 two-jaw gripper per loose thing, by type",
               basis="by geometry, not verified in simulation: the live agents confirm or reject each type",
               generator=os.path.abspath(__file__).replace("\\", "/"), module=os.path.join(HERE, "grasp_types.py").replace("\\", "/"),
               readme=os.path.join(HERE, "README_GRASPS.md").replace("\\", "/"), frame="scene frame of the pack (metres, Z up); episode world = scene - (0.90, 0.45)",
               gripper=GT.DEX1, counts_over_loose_things=counts, generated=time.strftime("%Y-%m-%d %H:%M"), objects=out)
    json.dump(res, open(os.path.join(HERE, "grasps_v2.json"), "w", encoding="utf-8"), indent=1)
    print(f"{len(out)} loose things, {time.time() - T0:.0f} s; things with a candidate of each type: {counts}")


if __name__ == "__main__":
    main()
