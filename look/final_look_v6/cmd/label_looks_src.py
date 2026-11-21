

# ----------------------------------------------------------------------------------------------------- v6 label / print textures
# v6 (20 Nov, AI-operated, render only): the bottles, cups, plates, bowls, chips can, cereal / toy boxes, books and toy blocks
# still read as flat colour at close-up distance. label_looks() gives each one a printed / glazed image (generic invented
# designs in look_tex/v6, made with an image model: no real brands) through its own primvar 'st_lbl' (the pack's 'st' and
# the other colour subsets stay as prop_looks() made them): cylindrical projection round the world up axis for bottles,
# cans and cups (label in a band, the palette colour above and below it; caps = the other colour subsets, untouched), a
# top-down planar projection for plates and bowls, a per-face box projection that fits the whole image on each side for
# boxes, books and blocks. Each image is colour-matched to the object's palette colour (k of the way) and written once per
# prop to look_tex/v6/applied.
LBL_DIR = f"{GEN_DIR}/v6"
_CUP = dict(band=(0.0, 1.0), rough=0.12, clearcoat=0.6)
# display -> (projection, image, options: band=(v0, v1) for cyl, match=k colour match, rough, clearcoat, cell=(cols, rows, i), rep)
LABELS = {
    "r71i1_lysol": ("cyl", "label_detergent", dict(band=(0.12, 0.70))),
    "r46i1_spray_bottle": ("cyl", "label_detergent", dict(band=(0.10, 0.60))),
    "r79i1_water_bottle": ("cyl", "label_water", dict(band=(0.30, 0.62))),
    "r115i1_bottle": ("cyl", "label_water", dict(band=(0.20, 0.60))),
    "r115i2_bottle": ("cyl", "label_water", dict(band=(0.20, 0.60))),
    "r75i1_bottle": ("cyl", "label_detergent", dict(band=(0.15, 0.62))),
    "r75i2_bottle": ("cyl", "label_detergent", dict(band=(0.15, 0.62))),
    "r182i1_bottle": ("cyl", "label_water", dict(band=(0.25, 0.65))),
    "r47i1_squeeze_bottle": ("cyl", "label_sauce", dict(band=(0.15, 0.70))),
    "r56i1_olive_oil": ("cyl", "label_oil", dict(band=(0.15, 0.62))),
    "r74i1_milk_jug": ("cyl", "label_water", dict(band=(0.25, 0.60))),
    "r155i1_kids_bottle": ("cyl", "label_water", dict(band=(0.20, 0.65))),
    "r72i1_chips_can": ("cyl", "chips_wrap", dict(band=(0.0, 1.0))),
    "r44i1_mug": ("cyl", "mug_print", dict(_CUP, match=0.3)),
    "r138i1_cup": ("cyl", "mug_print", dict(_CUP, match=0.3)),
    "r183i1_cup": ("cyl", "cup_glaze", dict(_CUP, match=0.8, rep=1)),
    "r197i1_cup": ("cyl", "cup_glaze", dict(_CUP, match=0.8, rep=1)),
    "r66i1_cup": ("cyl", "mug_print", dict(_CUP, match=0.5)),
    "r66i2_cup": ("cyl", "cup_glaze", dict(_CUP, match=0.8, rep=1)),
    "r66i3_cup": ("cyl", "mug_print", dict(_CUP, match=0.5)),
    "r66i4_cup": ("cyl", "cup_glaze", dict(_CUP, match=0.8, rep=1)),
    "r66i5_cup": ("cyl", "mug_print", dict(_CUP, match=0.5)),
    "r152i1_sippy_cup": ("cyl", "mug_print", dict(band=(0.05, 0.75), match=0.6, rough=0.3)),
    "r173i1_tumbler": ("cyl", "cup_glaze", dict(band=(0.0, 1.0), match=0.8, rough=0.15, rep=1)),
    "r49i1_canister": ("cyl", "cup_glaze", dict(_CUP, match=0.8, rep=1)),
    "r39i1_cereal": ("box", "cereal_box", dict(match=0.25)),
    "r39i2_cereal": ("box", "cereal_box", dict(match=0.25)),
    "r40i1_tea_box": ("box", "cereal_box", dict(match=0.5)),
    "r175i1_cardboard_box": ("box", "toy_box", dict(match=0.3)),
    "r150i1_small_box": ("box", "toy_box", dict(match=0.4)),
    "r88i1_small_box": ("box", "toy_box", dict(match=0.4)),
    "r88i2_small_box": ("box", "toy_box", dict(match=0.4)),
    "r50i1_blue_box": ("box", "toy_box", dict(match=0.5)),
    "r153i1_tissue_box": ("box", "toy_box", dict(match=0.5)),
    "r162i1_books": ("box", "book_spines", dict(match=0.3)),
    "r136i1_book": ("box", "book_covers", dict(match=0.4, cell=(2, 2, 0))),
    "r136i2_book": ("box", "book_covers", dict(match=0.4, cell=(2, 2, 1))),
    "r184i1_notebook": ("box", "book_covers", dict(match=0.5, cell=(2, 2, 2))),
    "r172i1_magazines": ("box", "book_covers", dict(match=0.4, cell=(2, 2, 3))),
    "r193i1_toy_piece": ("box", "block_letters", dict(match=0.6, cell=(3, 3, 0), rough=0.35)),
    "r193i2_toy_piece": ("box", "block_letters", dict(match=0.6, cell=(3, 3, 4), rough=0.35)),
    "r193i3_toy_piece": ("box", "block_letters", dict(match=0.6, cell=(3, 3, 6), rough=0.35)),
    "r193i4_toy_piece": ("box", "block_letters", dict(match=0.6, cell=(3, 3, 8), rough=0.35)),
}
for _n in ("r67i1_plate", "r67i2_plate", "r67i3_plate", "r67i4_plate", "r67i5_plate", "r67i6_plate", "r90i1_plate", "r91i1_tan_plate"):
    LABELS[_n] = ("top", "plate_top", dict(match=0.85, rough=0.1, clearcoat=0.7))
for _n in ("r65i1_bowl", "r65i2_bowl", "r65i3_bowl", "r65i4_bowl", "r177i1_bowl", "r89i1_salad_bowl", "r148i1_pink_lid"):
    LABELS[_n] = ("top", "bowl_top", dict(match=0.85, rough=0.1, clearcoat=0.7))


def _lbl_image(disp, img, opt, lin_rgb, circ_over_h):
    """Compose the per-prop image: colour-matched label (tiled round the body for cyl, inside its band) -> applied/<disp>.png."""
    from PIL import Image
    out_dir = f"{LBL_DIR}/applied"; os.makedirs(out_dir, exist_ok=True)
    path = f"{out_dir}/{disp}.png"
    im = Image.open(f"{LBL_DIR}/{img}.png").convert("RGB")
    if "cell" in opt:
        c, r, i = opt["cell"]; w, h = im.size; x, y = i % c, i // c
        im = im.crop((x * w // c, y * h // r, (x + 1) * w // c, (y + 1) * h // r))
    a = np.asarray(im, float) / 255.0
    pal = np.clip(np.asarray(lin_rgb, float), 0.02, 1) ** (1 / 2.2)            # sRGB of the palette colour
    k = float(opt.get("match", 0.15))
    a = np.clip(a * (1 - k + k * pal / max(a.reshape(-1, 3).mean(0), 1e-3)), 0, 1)
    if opt.get("_proj") == "cyl":
        v0, v1 = opt.get("band", (0.0, 1.0))
        rep = int(opt.get("rep") or max(1, round(circ_over_h / max(v1 - v0, 0.05) / (a.shape[1] / a.shape[0]))))
        lab = np.concatenate([a] * rep, axis=1)
        H, W = 1024, 2048
        bh = max(2, int(H * (v1 - v0)))
        lab = np.asarray(Image.fromarray((lab * 255).astype(np.uint8)).resize((W, bh)), float) / 255.0
        canvas = np.ones((H, W, 3)) * pal
        top = H - int(H * v1)                                                   # image row 0 = v 1
        canvas[top:top + bh] = lab[:H - top]
        a = canvas
    Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(path)
    return path


def label_looks(stage, top_path, usd_map=TL.USD_MAP, labels=LABELS, log=print):
    """Print / glaze images on the props of LABELS (render only: a primvar, a material, bindings). Idempotent."""
    M = _map(usd_map); done = {}; miss = []
    byname = {e["display"]: e for e in M["prims"]}
    for disp, (proj, img, opt) in labels.items():
        e = byname.get(disp); p = _tex_prim(stage, top_path, e) if e else None
        if p is None or not os.path.exists(f"{LBL_DIR}/{img}.png"):
            miss.append(disp); continue
        me = UsdGeom.Mesh(p)
        C = np.asarray(me.GetFaceVertexCountsAttr().Get(), int); I = np.asarray(me.GetFaceVertexIndicesAttr().Get(), int)
        X = UsdGeom.Xformable(p).ComputeLocalToWorldTransform(Usd.TimeCode.Default())
        Mx = np.array([[X[i][j] for j in range(4)] for i in range(4)])
        W = np.asarray(me.GetPointsAttr().Get(), float) @ Mx[:3, :3] + Mx[3, :3]   # world points (row vectors)
        lo, hi = W.min(0), W.max(0); ctr = (lo + hi) / 2; ext = np.maximum(hi - lo, 1e-4)
        subs = [s for s in UsdGeom.Subset.GetAllGeomSubsets(me) if s.GetPrim().GetName().startswith("fl_c")]
        body = None; lin = np.array([0.6, 0.6, 0.6])
        if subs:
            body = subs[int(np.argmax([len(s.GetIndicesAttr().Get()) for s in subs]))]
            lin = np.asarray(body.GetPrim().GetCustomDataByKey("fl_lin") or lin, float)
        else:
            fc = _face_colours(stage, p, e)
            if fc:
                lin = np.asarray(fc[int(np.argmax([len(g[2]) for g in fc]))][1], float)
        st = np.zeros((len(I), 2)); start = np.r_[0, np.cumsum(C)[:-1]]; circ_over_h = 1.0
        if proj == "cyl":
            th = np.arctan2(W[:, 1] - ctr[1], W[:, 0] - ctr[0]) / (2 * np.pi) + 0.5
            vz = (W[:, 2] - lo[2]) / ext[2]
            for s0, c in zip(start, C):
                ids = I[s0:s0 + c]; u = th[ids].copy()
                if u.max() - u.min() > 0.5:
                    u[u < 0.5] += 1.0
                st[s0:s0 + c, 0] = u; st[s0:s0 + c, 1] = vz[ids]
            circ_over_h = np.pi * 0.5 * (ext[0] + ext[1]) / ext[2]
        elif proj == "top":
            R = 0.5 * max(ext[0], ext[1])
            st[:, 0] = ((W[:, 0] - ctr[0]) / (2 * R) + 0.5)[I]; st[:, 1] = ((W[:, 1] - ctr[1]) / (2 * R) + 0.5)[I]
        else:
            for s0, c in zip(start, C):
                ids = I[s0:s0 + c]; q = W[ids]
                n = np.cross(q[1] - q[0], q[2] - q[0]) if c >= 3 else np.array([0, 0, 1.0])
                ax = int(np.argmax(np.abs(n)))
                a1, a2 = [a for a in range(3) if a != ax]                   # sides: horizontal axis = u, z = v
                st[s0:s0 + c, 0] = (q[:, a1] - lo[a1]) / ext[a1]; st[s0:s0 + c, 1] = (q[:, a2] - lo[a2]) / ext[a2]
        pv = UsdGeom.PrimvarsAPI(p).CreatePrimvar("st_lbl", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying)
        pv.Set(Vt.Vec2fArray.FromNumpy(st.astype(np.float32)))
        path = _lbl_image(disp, img, dict(opt, _proj=proj), lin, circ_over_h)
        mt = material(stage, f"lbl_{disp}", diffuse=path, rough=opt.get("rough", 0.35), varname="st_lbl",
                      clearcoat=opt.get("clearcoat", 0.0), clearcoat_rough=0.05)
        if body is not None:
            UsdShade.MaterialBindingAPI.Apply(body.GetPrim()).Bind(mt)
            if len(subs) == 1:
                UsdShade.MaterialBindingAPI.Apply(p).Bind(mt, UsdShade.Tokens.strongerThanDescendants)
        else:
            UsdShade.MaterialBindingAPI.Apply(p).Bind(mt, UsdShade.Tokens.strongerThanDescendants)
        done[disp] = img
    log(f"[final look] labels: {len(done)} props printed {sorted(set(done.values()))}; missing {miss}")
    return dict(done=done, missing=miss)
