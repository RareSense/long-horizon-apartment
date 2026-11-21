# PREVIEW STILLS (coordinator 20 Nov, AI-operated): textured room as the final video, higher RTX quality + a path-traced
# comparison; each still timed; settings restored at the end. Render only: physics not stepped.
import carb, time as _rt, json as _rj
from PIL import Image as _RI
OUTD = r"C:\Users\raresense\sim_home\apartment\final_look_preview"
S_ = carb.settings.get_settings()
KEYS = ["/rtx/rendermode", "/rtx/post/aa/op", "/rtx/post/dlss/execMode", "/rtx/reflections/enabled", "/rtx/translucency/enabled",
        "/rtx/shadows/enabled", "/rtx/indirectDiffuse/enabled", "/rtx/ambientOcclusion/enabled", "/rtx/directLighting/sampledLighting/enabled",
        "/rtx/pathtracing/spp", "/rtx/pathtracing/totalSpp", "/rtx/pathtracing/optixDenoiser/enabled", "/rtx/pathtracing/maxBounces",
        "/rtx/reflections/maxRoughness", "/rtx/raytracing/fractionalCutoutOpacity", "/rtx/directLighting/sampledLighting/samplesPerPixel"]
ORIG = {k_: S_.get(k_) for k_ in KEYS}
print("orig", ORIG, "textured env", os.environ.get("URC_TEXTURED"), flush=True)
sync_cloth(force=True); head_pose()
views0 = CAM.get("views")
for k_, c_ in CAM.items():                                      # the normal products off while the stills render
    if isinstance(c_, dict) and "rp" in c_:
        try: c_["rp"].hydra_texture.set_updates_enabled(False)
        except Exception: pass
pc_ = UsdGeom.Camera.Define(stage, "/World/PreviewCam"); pc_.CreateFocalLengthAttr(18.0); pc_.CreateClippingRangeAttr(Gf.Vec2f(0.05, 100))
pc_.CreateHorizontalApertureAttr(20.955); pc_.CreateVerticalApertureAttr(20.955 * 1080 / 1920)
UsdGeom.Xformable(pc_).ClearXformOpOrder(); pop_ = UsdGeom.Xformable(pc_).AddTransformOp()
hc_ = UsdGeom.Camera(stage.GetPrimAtPath("/World/HeadCam")); hva0_ = hc_.GetVerticalApertureAttr().Get(); hha0_ = hc_.GetHorizontalApertureAttr().Get()
TIMES = {}


def _prod(path):
    rp_ = rep.create.render_product(path, (1920, 1080)); an_ = rep.AnnotatorRegistry.get_annotator("rgb"); an_.attach([rp_])
    return rp_, an_


def _shot(name, path, n_warm, n_time, out):
    rp_, an_ = _prod(path)
    for _ in range(n_warm): app.update()
    t0_ = _rt.time()
    for _ in range(n_time): app.update()
    ms_ = (_rt.time() - t0_) * 1000.0 / n_time
    a_ = an_.get_data(); im_ = _RI.fromarray(np.ascontiguousarray(a_[..., :3]))
    im_.save(os.path.join(OUTD, out)); TIMES[out] = round(ms_, 1)
    try:
        an_.detach([rp_])
    except Exception:
        pass
    rp_.destroy()
    print(out, "ms/frame", round(ms_, 1), "mem", kit_mem(), flush=True)


def _rt_hq():
    S_.set("/rtx/rendermode", "RaytracedLighting"); S_.set("/rtx/post/aa/op", 4)   # DLAA (no DLSS upscaling)
    S_.set("/rtx/post/dlss/execMode", 2)
    for k_ in ("/rtx/reflections/enabled", "/rtx/translucency/enabled", "/rtx/shadows/enabled", "/rtx/indirectDiffuse/enabled",
               "/rtx/ambientOcclusion/enabled", "/rtx/directLighting/sampledLighting/enabled"):
        S_.set(k_, True)
    S_.set("/rtx/reflections/maxRoughness", 0.6)


try:
    _rt_hq()
    _shot("room", "/World/RoomCam", 40, 20, "room_rt_1080.png")
    hc_.GetVerticalApertureAttr().Set(hha0_ * 1080 / 1920)
    _shot("head", "/World/HeadCam", 40, 20, "head_rt_1080.png")
    hc_.GetVerticalApertureAttr().Set(hva0_)
    pop_.Set(Gf.Matrix4d().SetLookAt(Gf.Vec3d(-4.55, -0.75, 1.25), Gf.Vec3d(-5.18, -1.40, 0.08), Gf.Vec3d(0, 0, 1)).GetInverse())
    _shot("basket", "/World/PreviewCam", 40, 10, "closeup_toy_basket_rt_1080.png")
    pop_.Set(Gf.Matrix4d().SetLookAt(Gf.Vec3d(1.70, -1.30, 1.05), Gf.Vec3d(1.70, -2.10, 0.03), Gf.Vec3d(0, 0, 1)).GetInverse())
    _shot("mat", "/World/PreviewCam", 40, 10, "closeup_shoe_mat_rt_1080.png")
    S_.set("/rtx/rendermode", "PathTracing"); S_.set("/rtx/pathtracing/spp", 8); S_.set("/rtx/pathtracing/totalSpp", 64)
    S_.set("/rtx/pathtracing/optixDenoiser/enabled", True); S_.set("/rtx/pathtracing/maxBounces", 4)
    _shot("room_pt", "/World/RoomCam", 4, 8, "room_pt_1080.png")       # 8 frames x 8 spp = 64 spp, denoised
except Exception:
    import traceback as _tb; print("ERR", _tb.format_exc()[-1200:], flush=True)
finally:
    for k_, v_ in ORIG.items():
        if v_ is not None:
            S_.set(k_, v_)
    hc_.GetVerticalApertureAttr().Set(hva0_)
    for k_, c_ in CAM.items():
        if isinstance(c_, dict) and "rp" in c_:
            try: c_["rp"].hydra_texture.set_updates_enabled(views0 is None or k_ in views0)
            except Exception: pass
    for _ in range(5): app.update()
    print("restored", {k_: S_.get(k_) for k_ in KEYS[:3]}, flush=True)
_rj.dump(dict(ms_per_frame=TIMES, note="1920x1080, one view per measurement; RT = RaytracedLighting + DLAA, reflections/translucency/GI/AO/sampled lighting on; PT = PathTracing 8 spp/frame, 64 total, OptiX denoiser, 4 bounces (ms is per 8-spp frame; 64 spp = 8 frames)", state=state()),
         open(os.path.join(OUTD, "times.json"), "w"), indent=1)
print("TIMES", TIMES, flush=True)
