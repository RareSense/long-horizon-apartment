# FINAL LOOK v4 path-traced stills (AI-operated, render only; physics is not stepped). 1920x1080 PathTracing, SPP_ samples
# per still (one update of /rtx/pathtracing/spp after a camera move), OptiX denoiser, ACES tone map (RTX op 6) with the
# exposure set by /rtx/post/tonemap/filmIso (ISO_). ONE render product on /World/PreviewCam for the session (FL_RP).
# Camera look in post (cam_look): a slight bloom of the highlights, a mild vignette, faint sensor grain.
# Globals in: SHOTS_ (names or None = all), OUTD_ (folder), SPP_, ISO_ (ISO_VIEW_ per view), RAW_ (also save the un-post-processed frame).
import carb, time as _rt, json as _rj
from PIL import Image as _RI, ImageFilter as _RF
OUTD = globals().get("OUTD_") or r"C:\Users\raresense\sim_home\apartment\final_look_v4"
SHOTS_ = globals().get("SHOTS_"); SPP = int(globals().get("SPP_") or 64); ISO = float(globals().get("ISO_") or 100.0)
os.makedirs(OUTD, exist_ok=True)
S_ = carb.settings.get_settings()
for k_, c_ in CAM.items():
    if isinstance(c_, dict) and "rp" in c_:
        try: c_["rp"].hydra_texture.set_updates_enabled(False)
        except Exception: pass
pc_ = UsdGeom.Camera.Define(stage, "/World/PreviewCam")
UsdGeom.Xformable(pc_).ClearXformOpOrder(); pop_ = UsdGeom.Xformable(pc_).AddTransformOp()
if globals().get("FL_RP") is None:
    FL_RP = rep.create.render_product("/World/PreviewCam", (1920, 1080)); FL_AN = rep.AnnotatorRegistry.get_annotator("rgb"); FL_AN.attach([FL_RP])
    print("render product created (once)", kit_mem(), flush=True)
FL_RP.hydra_texture.set_updates_enabled(True)
VIEWS = {
    "photo418": ("room_photo161418_pt_1080.png", (4.1, -1.9, 1.55), (-0.5, 0.8, 0.6), 12.5),
    "photo423": ("room_photo161423_pt_1080.png", (3.3, -2.0, 1.5), (-6.3, -1.3, 1.0), 13.0),
    "photo414": ("kitchen_photo161414_pt_1080.png", (1.9, -0.9, 1.6), (3.8, 1.5, 0.8), 13.0),
    "room": ("room_photo161426_pt_1080.png", "/World/RoomCam"),
    "coffee": ("closeup_coffee_table_pt_1080.png", (-3.05, -1.75, 1.25), (-3.68, -0.91, 0.47), 20.0),
    "island": ("closeup_kitchen_counter_pt_1080.png", (2.95, -1.05, 1.65), (1.95, 0.05, 1.0), 18.0),
    "basket": ("closeup_toy_basket_pt_1080.png", (-4.55, -0.75, 1.25), (-5.18, -1.40, 0.08), 18.0),
    "mat": ("closeup_shoe_mat_pt_1080.png", (1.52, -1.30, 1.10), (1.52, -2.15, 0.02), 18.0),
}
VIEWS.update(globals().get("VIEWS_") or {})
# exposure per photo view (mean luma of each photo matched, 20 Nov): ISO 125 elsewhere
ISO_VIEW_ = dict({"photo418": 145.0, "photo423": 95.0, "photo414": 130.0, "room": 112.0}, **(globals().get("ISO_VIEW_") or {}))


def _copycam(src):
    c_ = UsdGeom.Camera(stage.GetPrimAtPath(src))
    pop_.Set(UsdGeom.Xformable(c_).ComputeLocalToWorldTransform(Usd.TimeCode.Default()))
    ha_ = c_.GetHorizontalApertureAttr().Get()
    pc_.GetFocalLengthAttr().Set(c_.GetFocalLengthAttr().Get()); pc_.GetHorizontalApertureAttr().Set(ha_)
    pc_.GetVerticalApertureAttr().Set(ha_ * 1080 / 1920); pc_.GetClippingRangeAttr().Set(c_.GetClippingRangeAttr().Get())


def _pv(eye, at, focal):
    pc_.CreateFocalLengthAttr().Set(float(focal)); pc_.CreateHorizontalApertureAttr().Set(20.955)
    pc_.CreateVerticalApertureAttr().Set(20.955 * 1080 / 1920); pc_.CreateClippingRangeAttr().Set(Gf.Vec2f(0.05, 100))
    pop_.Set(Gf.Matrix4d().SetLookAt(Gf.Vec3d(*map(float, eye)), Gf.Vec3d(*map(float, at)), Gf.Vec3d(0, 0, 1)).GetInverse())


def cam_look(a, bloom=0.06, thr=0.80, vig=0.22, grain=0.012, seed=3):
    """Phone-camera look on the tone-mapped 8-bit frame: bloom (blurred highlights above thr added back), radial
    vignette (vig = darkening at the corners), faint luminance grain."""
    f = a.astype(np.float32) / 255.0
    hi = np.clip(f - thr, 0, None) / (1 - thr)
    b = np.asarray(_RI.fromarray((hi * 255).astype(np.uint8)).filter(_RF.GaussianBlur(18)), np.float32) / 255.0
    f = f + bloom * b
    H, W = f.shape[:2]; yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2)
    f = f * (1 - vig * r ** 2.2)[..., None]
    f = f + grain * np.random.default_rng(seed).standard_normal((H, W, 1)).astype(np.float32)
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)


TIMES = {}
try:
    S_.set("/rtx/rendermode", "PathTracing"); S_.set("/rtx/pathtracing/spp", SPP); S_.set("/rtx/pathtracing/totalSpp", SPP)
    S_.set("/rtx/pathtracing/optixDenoiser/enabled", True); S_.set("/rtx/pathtracing/maxBounces", 4)
    S_.set("/rtx/post/tonemap/op", 6); S_.set("/rtx/post/tonemap/filmIso", ISO); S_.set("/rtx/post/histogram/enabled", False)
    for k_, v_ in VIEWS.items():
        if SHOTS_ is not None and k_ not in SHOTS_:
            continue
        S_.set("/rtx/post/tonemap/filmIso", float((globals().get("ISO_VIEW_") or {}).get(k_, ISO)))   # per view, like the phone's auto exposure
        if len(v_) == 2: _copycam(v_[1])
        else: _pv(v_[1], v_[2], v_[3])
        t0_ = _rt.time()
        for _ in range(3): app.update()
        a_ = np.ascontiguousarray(FL_AN.get_data()[..., :3])
        if globals().get("RAW_"):
            os.makedirs(os.path.join(OUTD, "raw"), exist_ok=True); _RI.fromarray(a_).save(os.path.join(OUTD, "raw", v_[0]))
        _RI.fromarray(cam_look(a_)).save(os.path.join(OUTD, v_[0])); TIMES[v_[0]] = round(_rt.time() - t0_, 1)
        print(v_[0], "s", TIMES[v_[0]], "mem", kit_mem(), flush=True)
except Exception:
    import traceback as _tb; print("ERR", _tb.format_exc()[-1500:], flush=True)
finally:
    FL_RP.hydra_texture.set_updates_enabled(False)
print("TIMES", TIMES, flush=True)
