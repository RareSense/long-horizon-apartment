# FINAL LOOK v3 stills (AI-operated, render only: physics is not stepped). 1920x1080 RaytracedLighting + DLAA with
# reflections / translucency / GI / AO / sampled lighting. ONE render product on /World/PreviewCam for the whole
# session (FL_RP / FL_AN in globals; each new one leaks ~0.3 GB); RoomCam / HeadCam shots copy that camera into
# PreviewCam. Globals in: SHOTS_ (list of names or None = all), OUTD_ (folder), VIEWS_ (optional dict overriding views).
import carb, time as _rt, json as _rj
from PIL import Image as _RI
OUTD = globals().get("OUTD_") or r"C:\Users\raresense\sim_home\apartment\final_look_v4"
SHOTS_ = globals().get("SHOTS_")
os.makedirs(OUTD, exist_ok=True)
S_ = carb.settings.get_settings()
KEYS = ["/rtx/rendermode", "/rtx/post/aa/op", "/rtx/post/dlss/execMode", "/rtx/reflections/enabled", "/rtx/translucency/enabled",
        "/rtx/shadows/enabled", "/rtx/indirectDiffuse/enabled", "/rtx/ambientOcclusion/enabled", "/rtx/directLighting/sampledLighting/enabled",
        "/rtx/reflections/maxRoughness"]
ORIG = {k_: S_.get(k_) for k_ in KEYS}
sync_cloth(force=True); head_pose()
views0 = CAM.get("views")
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
TIMES = {}
bb_ = centre(body_of("rubbish_bin")); hb_ = centre(body_of("r133i1_laundry_basket")); rb_ = base()[0]
# name -> (file, eye, at, focal) or (file, camera prim)
VIEWS = {
    "photo418": ("room_photo161418_rt_1080.png", (3.9, -1.6, 1.6), (-0.5, 1.6, 0.9), 12.0),   # from behind the island, as photo 20261117_161418
    "photo423": ("room_photo161423_rt_1080.png", (3.3, -2.0, 1.5), (-6.3, -1.3, 1.0), 13.0),    # hall end, down the room, as photo 161423
    "photo414": ("kitchen_photo161414_rt_1080.png", (1.9, -0.9, 1.6), (3.8, 1.5, 0.8), 13.0),    # kitchen, as photo 161414
    "room": ("room_rt_1080.png", "/World/RoomCam"),
    "head": ("head_rt_1080.png", "/World/HeadCam"),
    "basket": ("closeup_toy_basket_rt_1080.png", (-4.55, -0.75, 1.25), (-5.18, -1.40, 0.08), 18.0),
    "mat": ("closeup_shoe_mat_rt_1080.png", (1.70, -1.30, 1.05), (1.70, -2.10, 0.03), 18.0),
    "bin": ("closeup_rubbish_bin_rt_1080.png", tuple(np.r_[bb_[0] + 0.8, bb_[1] - 0.6, 1.2]), tuple(bb_), 24.0),
    "hamper": ("closeup_hamper_garments_rt_1080.png", tuple(np.r_[hb_[0] + 0.5, hb_[1] + 0.5, 1.5]), tuple(hb_), 24.0),
    "robot": ("closeup_robot_rt_1080.png", tuple(np.r_[rb_[:2] + np.array([1.2, 0.6]), 1.2]), tuple(np.r_[rb_[:2], 0.6]), 24.0),
    "sofa": ("detail_sofa_rug_floor_rt_1080.png", (-1.2, -0.4, 1.0), (-2.4, 0.6, 0.35), 24.0),
    "brick": ("detail_brick_window_curtain_rt_1080.png", (-3.2, -1.0, 1.6), (-5.4, -1.9, 1.5), 20.0),
    "cabinet": ("detail_kitchen_wood_granite_rt_1080.png", (3.3, 0.2, 1.5), (4.3, 1.6, 1.0), 20.0),
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


def _shot(v, n_warm=40, n_time=10):
    if len(v) == 2: _copycam(v[1])
    else: _pv(v[1], v[2], v[3])
    for _ in range(n_warm): app.update()
    t0_ = _rt.time()
    for _ in range(n_time): app.update()
    ms_ = (_rt.time() - t0_) * 1000.0 / n_time
    a_ = FL_AN.get_data(); _RI.fromarray(np.ascontiguousarray(a_[..., :3])).save(os.path.join(OUTD, v[0])); TIMES[v[0]] = round(ms_, 1)
    print(v[0], "ms/frame", round(ms_, 1), "mem", kit_mem(), flush=True)


try:
    S_.set("/rtx/rendermode", "RaytracedLighting"); S_.set("/rtx/post/aa/op", 4); S_.set("/rtx/post/dlss/execMode", 2)
    for k_ in ("/rtx/reflections/enabled", "/rtx/translucency/enabled", "/rtx/shadows/enabled", "/rtx/indirectDiffuse/enabled",
               "/rtx/ambientOcclusion/enabled", "/rtx/directLighting/sampledLighting/enabled"):
        S_.set(k_, True)
    S_.set("/rtx/reflections/maxRoughness", 0.6)
    for k_, v_ in VIEWS.items():
        if SHOTS_ is None or k_ in SHOTS_:
            _shot(v_)
except Exception:
    import traceback as _tb; print("ERR", _tb.format_exc()[-1500:], flush=True)
finally:
    for k_, v_ in ORIG.items():
        if v_ is not None:
            S_.set(k_, v_)
    FL_RP.hydra_texture.set_updates_enabled(False)
    for k_, c_ in CAM.items():
        if isinstance(c_, dict) and "rp" in c_:
            try: c_["rp"].hydra_texture.set_updates_enabled(views0 is None or k_ in views0)
            except Exception: pass
    for _ in range(3): app.update()
if SHOTS_ is None:
    _rj.dump(dict(ms_per_frame=TIMES, note="AI-operated. 1920x1080 RaytracedLighting + DLAA, reflections/translucency/GI/AO/sampled lighting on", state=state()),
             open(os.path.join(OUTD, "times.json"), "w"), indent=1)
print("TIMES", TIMES, flush=True)
