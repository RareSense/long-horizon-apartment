# FINAL LOOK v5 path-traced stills (AI-operated, render only; physics is not stepped). 1920x1080 PathTracing SPP_ spp,
# OptiX denoiser; tone map / exposure / bloom / vignette / grain from urc.tasks.home.final_look (camera_settings, cam_look).
import carb, time as _rt, importlib
from PIL import Image as _RI
import urc.tasks.home.final_look as FL5
OUTD = globals().get("OUTD_") or r"C:\Users\raresense\sim_home\apartment\final_look_v5"
SHOTS_ = globals().get("SHOTS_"); SPP = int(globals().get("SPP_") or 64)
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
FL_RP.hydra_texture.set_updates_enabled(True)
VIEWS = {
    "photo418": ("room_photo161418_pt_1080.png", (4.1, -1.9, 1.55), (-0.5, 0.8, 0.6), 12.5),
    "photo423": ("room_photo161423_pt_1080.png", (3.3, -2.0, 1.5), (-6.3, -1.3, 1.0), 13.0),
    "photo414": ("kitchen_photo161414_pt_1080.png", (1.9, -0.9, 1.6), (3.8, 1.5, 0.8), 13.0),
    "room": ("room_photo161426_pt_1080.png", "/World/RoomCam"),
    "island": ("closeup_kitchen_island_pt_1080.png", (2.95, -1.05, 1.65), (1.95, 0.05, 1.0), 18.0),
    "coffee": ("closeup_coffee_table_pt_1080.png", (-3.05, -1.75, 1.25), (-3.68, -0.91, 0.47), 20.0),
    "bags": ("closeup_bags_by_island_pt_1080.png", (3.9, -2.5, 1.45), (2.45, -0.55, 0.45), 15.0),
}
VIEWS.update(globals().get("VIEWS_") or {})


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


TIMES = {}
try:
    S_.set("/rtx/rendermode", "PathTracing"); S_.set("/rtx/pathtracing/spp", SPP); S_.set("/rtx/pathtracing/totalSpp", SPP)
    S_.set("/rtx/pathtracing/optixDenoiser/enabled", True); S_.set("/rtx/pathtracing/maxBounces", 4)
    for k_, v_ in VIEWS.items():
        if SHOTS_ is not None and k_ not in SHOTS_:
            continue
        FL5.camera_settings(k_, S_)
        if len(v_) == 2: _copycam(v_[1])
        else: _pv(v_[1], v_[2], v_[3])
        t0_ = _rt.time()
        for _ in range(3): app.update()
        a_ = np.ascontiguousarray(FL_AN.get_data()[..., :3])
        _RI.fromarray(FL5.cam_look(a_)).save(os.path.join(OUTD, v_[0])); TIMES[v_[0]] = round(_rt.time() - t0_, 1)
        print(v_[0], "s", TIMES[v_[0]], "mem", kit_mem(), flush=True)
except Exception:
    import traceback as _tb; print("ERR", _tb.format_exc()[-1500:], flush=True)
finally:
    FL_RP.hydra_texture.set_updates_enabled(False)
print("TIMES", TIMES, flush=True)
