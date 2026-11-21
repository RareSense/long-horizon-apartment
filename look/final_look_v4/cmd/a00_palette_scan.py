# AI-operated analysis (read only): per prop with a palette material, the palette colours its faces sample (face-centroid UV).
import json, collections, numpy as np
from pxr import Usd, UsdGeom, UsdShade
from PIL import Image
USD = "D:/apartment_real/textured/usd/apartment_1122.usdc"; TEX = "D:/apartment_real/textured/usd/textures/"
M = json.load(open("C:/Users/raresense/sim_home/apartment/textured_swap/usd_body_map.json", encoding="utf-8"))
st = Usd.Stage.Open(USD)
out = {}
for e in M["prims"]:
    mm = e.get("materials", [])
    if not mm: continue
    mn = mm[0]["material"].split("/")[-1]
    if not mn.startswith("Material_"): continue
    p = st.GetPrimAtPath(e["usd_prim"] + "/" + e["usd_meshes"][0]); me = UsdGeom.Mesh(p)
    C = np.array(me.GetFaceVertexCountsAttr().Get()); I = np.array(me.GetFaceVertexIndicesAttr().Get())
    P = np.array(me.GetPointsAttr().Get(), float)
    pv = UsdGeom.PrimvarsAPI(p).GetPrimvar("st")
    rec = dict(cls=e.get("cls"), mat=mn, n_faces=int(len(C)), size=[round(float(x), 3) for x in (P.max(0) - P.min(0))] if len(P) else None,
               subsets=[s.GetPrim().GetName() for s in UsdGeom.Subset.GetAllGeomSubsets(me)])
    sh = None
    for q in Usd.PrimRange(st.GetPrimAtPath(mm[0]["material"])):
        s_ = UsdShade.Shader(q)
        if s_ and s_.GetIdAttr().Get() == "UsdPreviewSurface": sh = s_
    if sh is not None:
        rec["metal"] = sh.GetInput("metallic").Get() if sh.GetInput("metallic") else None
        rec["rough"] = sh.GetInput("roughness").Get() if sh.GetInput("roughness") else None
        d = sh.GetInput("diffuseColor")
        if d and not d.HasConnectedSource(): rec["const"] = [round(float(x), 3) for x in d.Get()]
        op = sh.GetInput("opacity"); rec["opacity"] = op.Get() if op and not op.HasConnectedSource() else ("tex" if op else None)
    tx = mm[0].get("textures")
    if tx and pv:
        im = np.asarray(Image.open(TEX + tx[0].split("/")[-1]).convert("RGB")); H, W = im.shape[:2]
        uv = np.array(pv.ComputeFlattened(), float); interp = pv.GetInterpolation()
        k = 0; cols = collections.Counter(); 
        for f, c in enumerate(C):
            ids = I[k:k + c]
            q = uv[k:k + c] if interp == "faceVarying" else uv[ids]
            k += c
            u, v = q.mean(0); x = int(np.clip(u % 1.0 * W, 0, W - 1)) if u != 1 else W - 1; y = int(np.clip((1 - v % 1.0) * H, 0, H - 1))
            cols[tuple(int(a) for a in im[y, x])] += 1
        rec["palette"] = [[list(k_), n] for k_, n in cols.most_common()]
        rec["uv_interp"] = interp
    out[e["display"]] = rec
json.dump(out, open("C:/Users/raresense/sim_home/apartment/final_look_v4/cmd/palette_scan.json", "w"), indent=0)
for k_, r in out.items():
    print(k_, r["cls"], r["mat"], r.get("size"), r.get("subsets"), "metal", r.get("metal"), "rough", r.get("rough"), "op", r.get("opacity"), r.get("const"), (r.get("palette") or [])[:5])
