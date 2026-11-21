r"""Full tidy plan for Apartment 1122, v3 "LOOKS CLEAN" (planning only: NOTHING here is a simulation result).

    py -3.12 C:\Users\raresense\sim_home\apartment\full_plan\make_full_plan_v3.py         (writes the *_v3.* outputs)

v3 = v2 (make_full_plan.py; its outputs are left as they are) + everything else out of place gets a destination and a
method: the big floor things (scooters, the open umbrella, the cardboard box: carry2 / drag / push, with the forces at
the hand against the hold's limits), the towel and the coat as cloth, the strap, the stick, the kitchen things v2 left,
the open doors (dishwasher, TV-cabinet door) as close steps, the big things first in the route, and clean_targets_v3.json
(the expected end pose of EVERY loose thing, read by check_clean_look.py). Writes full_plan_v3.json, route_steps_v3.json,
room_patch_v3.json, clean_targets_v3.json, FULL_PLAN_v3.md. Memory: the process puts itself in a 2 GB job and runs at
below-normal priority; it refuses to start under 8 GB of available RAM.

v2's own text follows.

    py -3.12 C:\Users\raresense\sim_home\apartment\full_plan\make_full_plan.py            (writes the plan)
    py -3.12 ...\make_full_plan.py --reach 0.45 0.60 --dry                               (other reach limits: counts only)

Reads (never writes) D:\apartment_real\mujoco\unzipped\environment.xml + scene_spec.json, the floor agent's
navigation / grasp-geometry modules (E:\urc_home\src\urc\tasks\home\nav.py, grasp_geom.py; copies of both are kept
beside this script and used if the import fails), grasps_v2.json (make_grasps_v2.py: five grasp types),
hollow_colliders.json (make_hollow_colliders.py) and, when the cloth/surface agent names one in
C:\Users\raresense\sim_home\apartment\PROGRESS_CLOTH.md, its MEASURED reach map (JSON). Writes full_plan.json,
route_steps.json, room_patch.json and FULL_PLAN.md into this folder (v1 kept as *_v1.*).
Every reach / grasp judgement is BY GEOMETRY, NOT VERIFIED in simulation.
All coordinates are in the SCENE frame (the pack's frame, metres, Z up). The episode's world frame is the scene
moved by the robot start: world = scene - (0.90, 0.45)."""
import sys, os, json, math, time, itertools, collections, re


def _memory_guard(rss_gb=1.9, commit_gb=3.0, need_free_gb=8.0):
    """This PC runs two Isaac sessions: refuse to start under `need_free_gb` available; a watchdog ends this process
    if its resident memory passes `rss_gb` (the rule: no process over 2 GB); a Windows job caps its COMMITTED memory at
    `commit_gb` as a hard backstop (commit runs ahead of resident memory: numpy + MuJoCo reserve about 1.5 GB they never
    touch); one BLAS thread; below-normal priority."""
    for k_ in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[k_] = "1"
    if os.name != "nt":
        return
    import ctypes, ctypes.wintypes as wt, threading

    class PMC(ctypes.Structure):
        _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [(n, ctypes.c_size_t) for n in ("Peak", "WorkingSetSize", "a", "b", "c", "d", "e", "f")]

    def _watch():
        ps = ctypes.WinDLL("psapi"); kk = ctypes.WinDLL("kernel32"); kk.GetCurrentProcess.restype = wt.HANDLE
        ps.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.DWORD]
        while True:
            c = PMC(); c.cb = ctypes.sizeof(c); ps.GetProcessMemoryInfo(kk.GetCurrentProcess(), ctypes.byref(c), c.cb)
            if c.WorkingSetSize > rss_gb * 1024 ** 3:
                print(f"[memory guard] resident memory {c.WorkingSetSize / 1024 ** 3:.2f} GB > {rss_gb} GB: stopping", flush=True); os._exit(4)
            time.sleep(0.5)
    threading.Thread(target=_watch, daemon=True).start()
    limit_gb = commit_gb
    k = ctypes.WinDLL("kernel32", use_last_error=True)

    class MS(ctypes.Structure):
        _fields_ = [("dwLength", wt.DWORD), ("dwMemoryLoad", wt.DWORD)] + [(n, ctypes.c_ulonglong) for n in ("tp", "ap", "tf", "af", "tv", "av", "ae")]

    class BASIC(ctypes.Structure):
        _fields_ = [("a", ctypes.c_longlong), ("b", ctypes.c_longlong), ("LimitFlags", wt.DWORD), ("c", ctypes.c_size_t), ("d", ctypes.c_size_t),
                    ("e", wt.DWORD), ("f", ctypes.c_size_t), ("g", wt.DWORD), ("h", wt.DWORD)]

    class EXT(ctypes.Structure):
        _fields_ = [("basic", BASIC), ("io", ctypes.c_ulonglong * 6), ("ProcessMemoryLimit", ctypes.c_size_t), ("j", ctypes.c_size_t), ("k", ctypes.c_size_t), ("l", ctypes.c_size_t)]
    s = MS(); s.dwLength = ctypes.sizeof(s); k.GlobalMemoryStatusEx(ctypes.byref(s))
    if s.ap / 1024 ** 3 < need_free_gb:
        print(f"[memory guard] only {s.ap / 1024 ** 3:.1f} GB available (< {need_free_gb} GB): not starting"); sys.exit(3)
    k.GetCurrentProcess.restype = wt.HANDLE; k.CreateJobObjectW.restype = wt.HANDLE
    k.CreateJobObjectW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p]
    k.SetInformationJobObject.argtypes = [wt.HANDLE, ctypes.c_int, ctypes.c_void_p, wt.DWORD]
    k.AssignProcessToJobObject.argtypes = [wt.HANDLE, wt.HANDLE]; k.SetPriorityClass.argtypes = [wt.HANDLE, wt.DWORD]
    k.SetPriorityClass(k.GetCurrentProcess(), 0x4000)
    job = k.CreateJobObjectW(None, None); e = EXT(); e.basic.LimitFlags = 0x100; e.ProcessMemoryLimit = int(limit_gb * 1024 ** 3)
    ok = k.SetInformationJobObject(job, 9, ctypes.byref(e), ctypes.sizeof(e)) and k.AssignProcessToJobObject(job, k.GetCurrentProcess())
    print(f"[memory guard] {s.ap / 1024 ** 3:.1f} GB available; resident cap {rss_gb} GB (watchdog), commit cap {limit_gb} GB: {'on' if ok else 'NOT set'}; below-normal priority", flush=True)


_memory_guard()
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "D:/apartment_real/mujoco/unzipped"
import numpy as np, mujoco
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
try:
    sys.path.insert(0, "E:/urc_home/src")
    from urc.tasks.home import nav as NAV, grasp_geom as GG
    LOGIC = "imported read-only from E:/urc_home/src/urc/tasks/home (nav.py, grasp_geom.py)"
except Exception as ex:                                   # the other agent's tree is being edited: use the copies of 18 Nov (commit c2467f3)
    sys.path.insert(0, HERE)
    import nav_snapshot as NAV, grasp_geom_snapshot as GG
    LOGIC = f"copies beside this script (import from E:/urc_home failed: {ex})"
BASIS = "by geometry, not verified"
sys.path.insert(0, HERE)
import grasp_types as GT
GV2 = json.load(open(os.path.join(HERE, "grasps_v2.json"), encoding="utf-8"))["objects"]
HOLLOW = json.load(open(os.path.join(HERE, "hollow_colliders.json"), encoding="utf-8"))
DRY = "--dry" in sys.argv

# ---------------------------------------------------------------- numbers copied from E:\urc_home\scripts\home\skills.py (18 Nov)
R_BODY, R_FOOT = 0.28, 0.16                    # pelvis to furniture / to small things on the floor
X_REL, Y_REL = 0.17, 0.27                      # where a floor thing is put relative to the standing pelvis for a pick (measured reach map)
FOOT_X, FOOT_Y = (-0.075, 0.10), (0.085, 0.15)
START = np.array([0.90, 0.45])                 # robot start (scene frame); world = scene - START
OPEN_GAP = GG.OPEN_GAP                         # 7.9 cm between the pad faces (the task text says 8.2 cm maximum opening)
W_YES = OPEN_GAP - 2 * 0.0045                  # 7.0 cm: widest section the floor agent's grasp search accepts (clearance each side)
# ---------------------------------------------------------------- assumptions of THIS plan (not measured unless said)
MASS_NO, MASS_MARGINAL = 1.5, 0.8              # kg: over 1.5 not carried; 0.8-1.5 marginal for pad friction alone
REACH_YES, REACH_MARGINAL = 0.34, 0.50         # m, pelvis to the hand's target on furniture or over a container. 0.34 is MEASURED for the standing hand
#                                                (skills.DROP_X: from 0.38 the hand stayed 10 cm short); 0.50 with a trunk lean is ASSUMED
if "--reach" in sys.argv:                       # sensitivity runs: --reach YES MARGINAL
    _i = sys.argv.index("--reach"); REACH_YES, REACH_MARGINAL = float(sys.argv[_i + 1]), float(sys.argv[_i + 2])
REACH_ASSUMED = (REACH_YES, REACH_MARGINAL)
PROGRESS_CLOTH = "C:/Users/raresense/sim_home/apartment/PROGRESS_CLOTH.md"


def measured_reach_map():
    r"""HOOK for the cloth/surface agent's MEASURED furniture reach map. It is used when PROGRESS_CLOTH.md names an
    existing JSON with 'reach' in its file name (newest first). Expected rows (as its probe scripts\home\live\
    s10_reach_probe.py writes them): {z: pad height m, x: ahead m, y: to the hand's side m, err_xy, err_z, h: posture
    height, lean}. A row counts as reached when err_xy <= 1 cm and |err_z| <= 1.5 cm (the pick's own tolerances).
    Returns {source, levels: {z: (reach without lean m, reach with any posture m)}} or None (then the ASSUMED limits)."""
    try:
        txt = open(PROGRESS_CLOTH, encoding="utf-8").read()
    except OSError:
        return None
    paths = [p for p in re.findall(r"[A-Za-z]:[\\/][^\s`'\"<>|]*?reach[^\s`'\"<>|]*?\.json", txt, flags=re.I) if os.path.exists(p)]
    for p in sorted(set(paths), key=lambda p_: -os.path.getmtime(p_)):
        try:
            rows = json.load(open(p, encoding="utf-8"))
            rows = rows if isinstance(rows, list) else rows.get("rows", rows.get("points", []))
            lv = collections.defaultdict(lambda: [0.0, 0.0])
            for r in rows:
                if r.get("err_xy", 1) <= 0.01 and abs(r.get("err_z", 1)) <= 0.015:
                    dist = math.hypot(r["x"], r["y"]); z = round(float(r["z"]), 2)
                    lv[z][1] = max(lv[z][1], dist)
                    if not r.get("lean"):
                        lv[z][0] = max(lv[z][0], dist)
            if lv:
                return dict(source=p, levels={z: tuple(v) for z, v in sorted(lv.items())})
        except Exception:
            continue
    return None


REACH_MAP = measured_reach_map()


def reach_limits(z):
    """(yes, marginal, source) for a hand target at height z: the measured map's nearest level within 15 cm, else ASSUMED."""
    if REACH_MAP:
        zs = [k for k in REACH_MAP["levels"] if abs(k - z) <= 0.15]
        if zs:
            k = min(zs, key=lambda k_: abs(k_ - z)); y_, m_ = REACH_MAP["levels"][k]
            return y_, max(m_, y_), f"MEASURED ({os.path.basename(REACH_MAP['source'])}, pad height {k:.2f} m)"
    return REACH_YES, REACH_MARGINAL, "ASSUMED"
TOP_GRASP_MAX_Z = 0.95                         # m: a top-down grasp needs the wrist about 10 cm above the thing's top; ASSUMED limit for the standing G1
SIDE_MIN_H = 0.04                              # m: a side grasp needs this much height for the 2.9 cm pads
T = dict(                                       # seconds
    floor_pick=16.0, put_down=12.0,            # measured, run 1118_193303 (B)
    floor_pick_B2=18.0, put_down_B2=20.0,      # measured, run 1118_204943 (B2, the code as committed)
    cloth_pick=30.0, cloth_pick_two_hands=45.0,  # ASSUMED (cloth agent has no timed pick yet)
    surface_pick=20.0,                         # ASSUMED (skill not built)
    drop_in=8.0, place_on=12.0, sink_drop=10.0,  # ASSUMED (drop_in ran only in the practice room; others not built)
    container_pick=25.0, container_set=15.0,   # ASSUMED (two hands on opposite walls; not built)
    close_dishwasher=60.0)                     # ASSUMED (push two racks in, lift the door: not built)
V = dict(stated=dict(empty=0.45, carry=0.18),   # gait speeds given in the brief (empty: 0.35 asked = 0.45 real; carrying 0.18)
         b2=dict(empty=4.2 / 36.0, carry=7.0 / 111.0))   # end-to-end rates of run B2: 4.2 m of legs in 36 s empty, 7 m in 111 s carrying
TARGET_ITEM = (20.0, 30.0)                     # the user's target per item
TARGET = dict(empty=0.45, carry=0.45, container_pick=10.0, container_set=8.0)

# ---------------------------------------------------------------- the scene
spec = json.load(open(SRC + "/scene_spec.json", encoding="utf-8"))
m = mujoco.MjModel.from_xml_path(SRC + "/environment.xml"); d = mujoco.MjData(m); mujoco.mj_forward(m, d)


class Obj:
    pass


OBJ, BY_ID = {}, {}
for o in spec["objects"]:
    q = Obj(); b = np.asarray(o["bounds_m"], float); body = o.get("body") or {}
    q.id, q.name, q.cls = o["id"], o["name"], o["semantic_class"]
    q.motion = body.get("motion", "static"); q.mass = body.get("mass")
    q.lo, q.hi = b[0], b[1]; q.c = (b[0] + b[1]) / 2; q.size = b[1] - b[0]
    q.free = q.motion == "free"
    OBJ[q.name] = q; BY_ID[q.id] = q
FREE = [q for q in OBJ.values() if q.free]
assert len(FREE) == 198, len(FREE)
for q in FREE:
    q.P = GG.body_points(m, d, m.body(q.id + "_body").id)
    if len(q.P):                                         # the collision shape as it lies (the spec's box is the visual one)
        q.plo, q.phi = q.P.min(0), q.P.max(0)
    else:
        q.plo, q.phi = q.lo, q.hi

# garments that are real cloth in our model (cloth agent, E:\urc_cloth\rooms\apartment_1122_cloth.json)
CLOTH = ["r131i1_knit_hat", "r189i1_santa_hat", "r190i1_stocking", "r121i1_jacket", "r116i1_coat_pile", "r117i1_blanket", "r68i1_rag"]
CLOTH_BIG = ["r121i1_jacket", "r116i1_coat_pile", "r117i1_blanket"]
# v3: the towel over the stool and the coat over the armchair become cloth like the 7 garments (PROPOSED: the cloth
# agent's cloth.py has no pattern for them yet; a towel is one flat panel, the coat is the jacket pattern scaled up)
CLOTH_V3_NEW = ["r100i1_towel", "r165i1_coat"]
CLOTH = CLOTH + CLOTH_V3_NEW
CLOTH_BIG = CLOTH_BIG + ["r165i1_coat"]                    # 1.1 kg, 52 x 65 cm: both hands, one trip
CLOTH_ON_FURNITURE = {"r100i1_towel": "r99i2_stool", "r165i1_coat": "r164i1_chair"}   # cloth picks from furniture (not built)
BIN = dict(name="rubbish_bin", xy=np.array([1.00, 1.93]), size=[0.32, 0.32, 0.40], mass=1.5)

# ---------------------------------------------------------------- what each thing rests on
NOT_SUPPORT = ("floor", "ceiling", "wall", "scenery", "rug", "skirting", "light_fixture", "curtain_rail", "duct", "curtain", "glass")


def support_of(o):
    if o.lo[2] < 0.04:
        on = [q.name for q in OBJ.values() if q.cls == "rug" and q is not o and np.all(o.c[:2] > q.lo[:2]) and np.all(o.c[:2] < q.hi[:2])]
        return dict(type="floor", support="floor" + (f" (on {on[0]}, 1 cm)" if on else ""), surface_height_m=0.0)
    best = None
    for q in OBJ.values():
        if q is o or q.cls in NOT_SUPPORT:
            continue
        if np.all(o.c[:2] > q.lo[:2] - 0.02) and np.all(o.c[:2] < q.hi[:2] + 0.02):
            dz = o.lo[2] - q.hi[2]
            if -0.06 < dz < 0.04:
                k = (0, abs(dz), q)
            elif q.lo[2] - 0.02 < o.lo[2] < q.hi[2]:
                k = (1, float(np.prod(q.size)), q)
            else:
                continue
            if best is None or k[:2] < best[:2]:
                best = k
    if best is None:
        return dict(type="surface", support="unknown", surface_height_m=round(float(o.lo[2]), 2))
    return dict(type="surface" if best[0] == 0 else "inside", support=best[2].name, surface_height_m=round(float(o.lo[2]), 2))


def band(z):
    if z < 0.04:
        return "floor"
    if z < 0.35:
        return "low shelf 0.10-0.35 m (deep squat, reach in sideways)"
    if z < 0.62:
        return "low table / seat 0.45-0.56 m (half squat)"
    if z < 0.85:
        return "table / sill 0.72-0.78 m (standing)"
    if z < 1.05:
        return "counter 0.91-0.95 m (standing, hand at chest height)"
    return "above reach (over 1.2 m)"


for o in FREE:
    o.rest = support_of(o)

# ---------------------------------------------------------------- the tidy rules (TIDY_PLAN.md + common sense). One line per moved thing.
TOY, RUB, MAT, HAM, SINK, ISL, CON, TRAY, CORNER = "toy_basket", "bin", "mat", "hamper", "sink", "island", "console", "tray_table", "toy_corner"
MOVE = {
    # toys -> toy basket r186 (TIDY_PLAN); the two big ones do not fit a 33 x 27 x 12 cm basket -> the toy corner beside it
    "r120i1_duck": TOY, "r120i2_duck": TOY, "r174i1_plush": TOY, "r191i1_toy_vehicle": TOY, "r192i1_ball": TOY,
    "r193i1_toy_piece": TOY, "r193i2_toy_piece": TOY, "r193i3_toy_piece": TOY, "r193i4_toy_piece": TOY, "r190i1_stocking": TOY,
    "r139i1_toy_car": TOY, "r178i1_ball": TOY, "r93i1_nugget": TOY, "r179i1_toy_pouch": TOY,
    "r188i1_dollhouse": CORNER, "r130i1_light_saber": CORNER,
    # rubbish -> the added bin (ONLY rubbish goes there)
    "r195i1_paper": RUB, "r195i2_paper": RUB, "r195i3_paper": RUB, "r196i1_plastic_bag": RUB,
    "r69i1_scrap": RUB, "r69i2_scrap": RUB, "r69i3_scrap": RUB, "r69i4_scrap": RUB,
    "r157i1_paper": RUB, "r157i2_paper": RUB, "r158i1_tissue": RUB, "r149i1_pouch": RUB, "r87i1_wrapper": RUB,
    # shoes -> the doormat, in pairs
    "r105i1_shoe": MAT, "r105i2_shoe": MAT, "r122i1_croc": MAT, "r123i1_slipper": MAT, "r124i1_sandal": MAT,
    "r125i1_flat": MAT, "r125i2_flat": MAT,
    # garments (real cloth) -> the open-top laundry hamper
    "r131i1_knit_hat": HAM, "r189i1_santa_hat": HAM, "r121i1_jacket": HAM, "r116i1_coat_pile": HAM, "r117i1_blanket": HAM, "r68i1_rag": HAM,
    # used dishes -> the kitchen sink
    "r173i1_tumbler": SINK, "r197i1_cup": SINK, "r146i1_bowl": SINK, "r148i1_pink_lid": SINK, "r151i1_spoon": SINK, "r152i1_sippy_cup": SINK,
    "r155i1_kids_bottle": SINK, "r147i1_purple_container": SINK, "r138i1_cup": SINK, "r171i1_glass": SINK, "r177i1_bowl": SINK, "r183i1_cup": SINK,
    "r63i1_glass": SINK, "r81i1_glass_spoon": SINK, "r89i1_salad_bowl": SINK, "r90i1_plate": SINK, "r91i1_tan_plate": SINK,
    "r78i1_kids_bottle": SINK, "r92i1_pink_container": SINK,
    # food and drink left in the living room -> the kitchen island
    "r156i1_clementines": ISL, "r182i1_bottle": ISL,
    # small personal things -> the console table at the entry
    "r108i1_scissors": CON, "r107i1_umbrella": CON, "r176i1_cap": CON,
    # cleaning things left on the food island -> the tray table beside the mop (cleaning corner)
    "r71i1_lysol": TRAY, "r83i1_sponges": TRAY, "r83i2_sponges": TRAY,
}
WHY_MOVE = {TOY: "toy lying about: toys go in the toy basket", CORNER: "big toy on the rug: too big for the 33 x 27 x 12 cm basket, stands beside it",
            RUB: "rubbish (crumpled paper, wrapper, scrap, empty pouch, tissue): the bin", MAT: "shoe lying about: shoes stand in pairs on the doormat",
            HAM: "garment on the floor: the laundry hamper", SINK: "used dish away from the kitchen: the sink",
            ISL: "food / drink left in the living room: the kitchen island", CON: "small personal thing on the floor or a sill: the console table at the entry",
            TRAY: "cleaning thing left on the food island: the tray table at the cleaning corner (mop, cloth)"}
# mess that the plan does NOT move, with the plain reason
MESS_SKIPPED = {
    "r74i1_milk_jug": "belongs in the fridge: needs the fridge door opened (doors are frozen in our model, no door skill) and 1.2 kg is marginal for the jaws",
    "r165i1_coat": "coat thrown over the armchair; belongs on the hook rack r97 (1.3-2.4 m up, out of reach). It is a rigid drape shape in our model (not one of the 7 cloth garments), 1.1 kg",
    "r100i1_towel": "towel thrown over the stool; a rigid drape shape in our model (not cloth), 53 cm wide: nothing the jaws can take. If it were made cloth it would go to the hamper",
    "r194i1_strap": "strap on the rug: 1 cm thin, nothing for the pads to bite (TIDY_PLAN leaves cords and straps in phase 1)",
    "r198i1_cord": "cord on the floor: 1 cm thin, left (TIDY_PLAN)", "r198i2_cord": "cord on the floor: 1 cm thin, left (TIDY_PLAN)",
    "r161i1_hair_dryer": "hair dryer on the TV cabinet: belongs in a bathroom or a drawer; the scene has no bathroom and drawers are frozen: left",
    "r77i1_iron": "iron on the kitchen island: no better open place in the scene (cabinets need doors), 1.3 kg: left",
    "r70i1_tote": "tote bag on the kitchen island: 41 cm wide, 0.9 kg, no part the jaws can take from the side at 0.91 m: left",
    "r86i1_cables": "cable bundle on the island: 1.4 cm flat, no destination without a drawer: left",
    "r154i1_stick": "60 cm stick on the coffee table: 1 cm thin, nothing for the pads; left",
    "r106i1_umbrella": "large open umbrella on the floor (89 x 69 cm): too big to carry between the furniture; left (TIDY_PLAN)",
    "r175i1_cardboard_box": "cardboard box by the armchair: 28 x 24 x 25 cm, bigger than the bin's opening; a box that stays (TIDY_PLAN)",
}
IN_PLACE = {
    "r187i1_plush": "already in the toy basket", "r124i2_sandal": "already on the doormat (its partner r124i1 is brought to it)",
    "r136i1_book": "bottom of the two-book stack on the side table: already stacked", "r136i2_book": "top of the two-book stack on the side table: already stacked",
    "r162i1_books": "stack of books on the TV cabinet: tidy as it is", "r172i1_magazines": "magazines on the lower shelf of the two-tier table: where they belong",
    "r170i1_remote": "remote on the two-tier table beside the armchair: a sensible place (TIDY_PLAN's coffee table is only for a remote found elsewhere)",
    "r153i1_tissue_box": "tissue box on the coffee table: stays", "r150i1_small_box": "small box on the coffee table: not rubbish, not a dish; stays",
    "r44i1_mug": "mug on the counter at the sink: already at the sink", "r43i1_measuring_cup": "beside the dish basket: in place",
    "r49i1_canister": "storage canister on the cutting board by the range: in place",
    "r184i1_notebook": "notebook beside the keyboard on the window sill (work spot): stays",
    "r180i1_keyboard": "keyboard on the window sill (work spot): stays", "r181i1_mouse": "mouse on the window sill (work spot): stays",
    "r95i1_purple_cloth": "folded cleaning cloth on the tray table beside the mop: in place",
    "r119i1_mat": "the doormat itself (destination of the shoes)", "r186i1_basket": "the toy basket (destination; carried to the rug toys and back)",
    "r133i1_laundry_basket": "the laundry hamper (destination; open-top one of the same size in our model)", "r42i1_dish_basket": "dish basket on the counter: in place",
    "r185i1_megabloks_bag": "megabloks bag in the toy corner: in place (overflow for toys)",
}
for n in list(OBJ):
    if n.startswith(("r65i", "r66i", "r67i")):
        IN_PLACE[n] = "in the open dishwasher's pulled-out rack: where dishes belong (pushing the racks in and closing the door needs the drawer / door skill)"
    if n.startswith("r64i"):
        IN_PLACE[n] = "on top of the fridge (1.78 m): storage, and out of reach"
    if n.startswith("r163i"):
        IN_PLACE[n] = "in a cubby of the TV cabinet: where it belongs"
    if n.startswith("r144i"):
        IN_PLACE[n] = "sofa cushion on the sofa: in place"
LEAVE_CLS = {
    "appliance": "appliance standing where it is used: stays", "bag": "standing bag by the wall: stays (TIDY_PLAN)", "plant": "plant: stays",
    "table": "furniture: stays", "stool": "furniture: stays", "stroller": "stroller parked at the entry: stays", "lamp": "floor lamp: stays",
    "toy_vehicle": "scooter / bike standing: 2.2-3 kg, too heavy and big for the jaws; stays (TIDY_PLAN)", "decor": "decor: stays",
    "electronics": "electronics: stay", "cookware": "cookware on the range: in place", "kitchenware": "on the kitchen counter: in place",
    "hook_rack": "hook rack on the closet door: fixture", "tool": "stands / lies where it is kept: stays", "food": "food on the kitchen counter / island: in place",
    "food_package": "snack on the kitchen counter / island: food, not rubbish: stays", "package": "stays", "container": "kitchen / storage item where it is used: in place",
    "dish": "dish in the kitchen: in place", "cushion": "in place", "basket": "container: stays", "book": "in place", "umbrella": "stays", "rug": "stays",
    "textile": "stays", "clothing": "stays", "paper": "stays", "toy": "stays", "cable": "stays", "cutlery": "stays", "shoe": "stays",
}
# ---------------------------------------------------------------- v3 "looks clean": everything else out of place gets a place and a method
PARK, ENTRY, BOXW, BAGS, TVTOP, FRIDGE, UMBW = "vehicle_corner", "entry_floor", "box_wall", "bag_row", "tv_cabinet_top", "fridge", "umbrella_place"
V3_MOVE = {
    # big floor things (methods: carry2 / drag / push, see BIG below). Scooters parked nose-in against the hall wall beside the bike
    "r127i1_scooter": PARK, "r126i1_scooter": PARK,
    "r106i1_umbrella": UMBW, "r107i1_umbrella": ENTRY,       # umbrellas: the small one by the entry; the big open one (it cannot be closed) where it blocks nothing
    "r175i1_cardboard_box": BOXW,                             # pushed against the brick wall beside it
    # soft things v2 left: cloth now (PROPOSED), to the hamper; the strap (1.2 cm) to the hamper too
    "r100i1_towel": HAM, "r165i1_coat": HAM, "r194i1_strap": HAM,
    # the 60 cm stick on the coffee table: toy corner floor, like the light saber
    "r154i1_stick": CORNER,
    # kitchen things v2 left
    "r70i1_tote": BAGS,                                       # a bag: stands with the other bags on the floor
    "r77i1_iron": TRAY,                                       # laundry / cleaning corner (tray table beside the mop)
    "r86i1_cables": TVTOP,                                    # cable bundle: beside the TV on the TV cabinet
    "r74i1_milk_jug": FRIDGE,                                 # OPTIONAL round: needs the fridge door opened and closed
}
MOVE.update(V3_MOVE)
WHY_MOVE.update({PARK: "scooter standing in a walkway: parked upright, nose to the hall wall, beside the bike (vehicle corner)",
                 ENTRY: "umbrella on the floor in the way: by the entry, clear of the front door's swing",
                 BOXW: "cardboard box standing loose by the two-tier table: pushed square against the brick wall beside it",
                 BAGS: "bag on the kitchen island: stands on the floor with the other bags",
                 TVTOP: "cable bundle on the food island: beside the TV",
                 FRIDGE: "milk jug left out: the fridge (OPTIONAL: needs the door skill)",
                 UMBW: "large open umbrella lying in the passage between the island and the stroller: flat against a wall where it blocks no walking route",
                 HAM: WHY_MOVE[HAM], TRAY: WHY_MOVE[TRAY] + " (the iron: laundry things go to the same corner)", CORNER: WHY_MOVE[CORNER]})
for n_ in V3_MOVE:
    MESS_SKIPPED.pop(n_, None)
MESS_SKIPPED.update({
    "r161i1_hair_dryer": "hair dryer on the TV cabinet top: belongs in a bathroom or a drawer; there is no bathroom and no hollow storage the robot can open (the storage ottoman's base is solid in the collision model, ray-tested): left on the cabinet top beside the books",
})
for n_ in ("r198i1_cord", "r198i2_cord"):
    MESS_SKIPPED.pop(n_, None)                             # v3: power cords where they belong (below), not mess
IN_PLACE.update({
    "r128i1_bike": "toy bike already standing along the hall wall (15 cm off the baseboard) beside the robot vacuum: it is the west end of the vehicle corner the scooters are parked in; left",
    "r198i1_cord": "the heater's power cord (one end at the heater r132, the other at the wall, by geometry): where a plugged-in cord belongs; left",
    "r198i2_cord": "a power cord plugged into the outlet r19i7 (one end 1 cm from it) running along the planter: where it belongs; left",
})
for n_ in [n for n in OBJ if n.startswith("r144i")]:
    IN_PLACE[n_] = "sofa cushion upright against the sofa back: all three at the same height and yaw (0 deg, 0 deg tilt), evenly spaced 0.567 m: in place, not touched"
for o in FREE:
    if o.name in MOVE:
        o.status, o.dest, o.reason = "mess_to_move", MOVE[o.name], WHY_MOVE[MOVE[o.name]]
    elif o.name in MESS_SKIPPED:
        o.status, o.dest, o.reason = "mess_but_left", None, MESS_SKIPPED[o.name]
    elif o.name in IN_PLACE:
        o.status, o.dest, o.reason = "already_in_place", None, IN_PLACE[o.name]
    else:
        o.status, o.dest, o.reason = "leave", None, LEAVE_CLS.get(o.cls, "stays") + f" ({o.rest['support']})"
MESS = [o for o in FREE if o.status == "mess_to_move"]

# ---------------------------------------------------------------- grasp by geometry
def grasp_info(o):
    """Top-down sections (the floor agent's search, unchanged) and the narrowest side-on silhouette."""
    P = o.P
    g = dict(top=None, side_w=None, side_axis=None, options=[])
    if not len(P) or (o.mass or 0) > 3.0:
        return g
    zs = max(0.0, float(P[:, 2].min()))
    G = GG.find(P, zs)
    g["tight"] = False
    if not G:                                             # no section with the search's 4.5 mm clearance a side: one that just fits the open jaws?
        G = GG.find(P, zs, clearance=0.0005); g["tight"] = bool(G)
    if G:
        g["top"] = G[0]
        seen = set()
        for c in G:                                       # the best section per closing direction that is nearly as good (as skills.grasp_plan)
            k = int(round(math.degrees(math.atan2(c["close"][1], c["close"][0])) / 10.0)) % 18
            if k not in seen and c["score"] < G[0]["score"] + 0.03:
                seen.add(k); g["options"].append(c)
    best = None
    for k in range(36):
        a = math.pi * k / 36; u = np.array([math.cos(a), math.sin(a)])
        w = float(np.ptp(P[:, :2] @ u))
        if best is None or w < best[0]:
            best = (w, a)
    g["side_w"], g["side_axis"] = best
    return g


TYPE_ORDER_FLOOR = ("top_down", "surface_pinch", "side", "rim_pinch")
TYPE_ORDER_SURF = ("top_down", "side", "surface_pinch", "rim_pinch", "edge")
FINGERS_DOWN = ("top_down", "surface_pinch", "rim_pinch")
TYPE_SKILL = {"top_down": "fingers-down pick (floor: exists, run 1118_193303; from furniture: not built)",
              "surface_pinch": "NEW: fingertips on the support while the jaws close (not built)",
              "side": "NEW: side grasp, hand level, jaws horizontal (not built)",
              "rim_pinch": "NEW: rim pinch, jaws part-open, one inside (not built; needs the hollow collider)",
              "edge": "NEW: edge grasp, jaws vertical under an overhang, after a slide when needed (not built)",
              "cloth": "cloth pinch (cloth agent's grasp_cloth, written from its live knit-hat runs, commit cf4eabf)"}


def usable(o):
    """All grasp candidates of grasps_v2.json usable by geometry (before reach): [(type, candidate, verdict, notes)]."""
    e = GV2.get(o.name); out = []
    if e is None:
        return out
    floor = o.rest["type"] == "floor"; top_z = float(o.phi[2])
    for t in (TYPE_ORDER_FLOOR if floor else TYPE_ORDER_SURF):
        for c in e["grasps"].get(t, []):
            if c["verdict"] not in ("yes", "marginal"):
                continue
            v = c["verdict"]; notes = list(c["notes"])
            if not floor and t in FINGERS_DOWN and top_z > TOP_GRASP_MAX_Z:
                v = "marginal"; notes.append(f"fingers down with its top {top_z:.2f} m up: the wrist about {top_z + 0.10:.2f} m (ASSUMED limit {TOP_GRASP_MAX_Z + 0.10:.2f} m)")
            if floor and t == "side":
                v = "marginal"; notes.append("side grasp at floor level: hand level a few cm above the floor in the deep squat (not measured)")
            out.append((t, c, v, notes))
    return out


def type_rank(o, t):
    order = TYPE_ORDER_FLOOR if o.rest["type"] == "floor" else TYPE_ORDER_SURF
    return order.index(t) if t in order else 9


def grasp_verdict(o):
    """v2: the best grasp over the five types (by geometry, not verified). Reach may later pick another usable one."""
    out = dict(basis=BASIS)
    if o.name in CLOTH:
        return dict(out, verdict="yes", type="cloth", approach="cloth pinch from above", why="real cloth in our model: the jaws pinch a fold (cloth agent's grasp_cloth); ASSUMED graspable for all 7",
                    types={"cloth": "yes"})
    e = GV2.get(o.name, {})
    types = {}
    for t in GT.ORDER:
        vs = {c["verdict"] for c in e.get("grasps", {}).get(t, [])}
        types[t] = "yes" if "yes" in vs else ("marginal" if "marginal" in vs else ("no" if vs else "none"))
    if (o.mass or 0) > MASS_NO:
        return dict(out, verdict="no", type=None, why=f"too heavy: {o.mass:.2f} kg (limit about {MASS_NO} kg)", types=types, why_not_by_type=e.get("why_not", {}))
    U = usable(o)
    if not U:
        h = float(o.phi[2] - o.plo[2]); g = o.g
        if h < 0.010:
            why = f"too thin: {100 * h:.1f} cm high: no grasp type has anything for the pads (fingertips on the support need 1 cm; flat on the floor there is no edge)"
        elif g.get("side_w") is not None and g["side_w"] > OPEN_GAP:
            why = f"too wide: narrowest silhouette {100 * g['side_w']:.0f} cm (jaws 7.9 cm), no rim, edge or section any of the five types can take"
        else:
            why = "no section, rim or edge any of the five grasp types can take"
        if o.name in HOLLOW["kept_solid"]:
            why += f"; rim pinch: {HOLLOW['kept_solid'][o.name]}"
        return dict(out, verdict="no", type=None, why=why, types=types, why_not_by_type=e.get("why_not", {}))
    U.sort(key=lambda r: (r[2] != "yes", type_rank(o, r[0]), r[1]["score"]))
    t, c, v, notes = U[0]
    if (o.mass or 0) > MASS_MARGINAL:
        v = "marginal"; notes = notes + [f"{o.mass:.2f} kg: heavy for pad friction alone (measured squeeze 6 N a pad)"]
    return dict(out, verdict=v, type=t, approach=t, axis_deg=round(math.degrees(math.atan2(c["close"][1], c["close"][0]))) % 180, width_cm=round(100 * c["width_m"], 1),
                why="; ".join(notes), types=types, skill=TYPE_SKILL[t], new_type=t != "top_down", needs=c.get("needs", []),
                why_not_by_type=e.get("why_not", {}))


def grasp_verdict_v1(o):
    g = o.g; h = float(o.phi[2] - o.plo[2]); out = dict(basis=BASIS)
    floor = o.rest["type"] == "floor"
    if o.name in CLOTH:
        return dict(out, verdict="yes", approach="cloth pinch from above", axis_deg=None, width_cm=None,
                    why="real cloth in our model: the jaws pinch a fold (cloth_pick, cloth agent); the pack's rigid drape shape is not used. ASSUMED graspable; the cloth grasp is not proven yet")
    if (o.mass or 0) > MASS_NO:
        return dict(out, verdict="no", approach=None, axis_deg=None, width_cm=None, why=f"too heavy: {o.mass:.2f} kg (limit about {MASS_NO} kg)")
    top = g["top"]; top_z = float(o.phi[2])
    side_ok = (not floor) and g["side_w"] is not None and g["side_w"] <= OPEN_GAP and h >= SIDE_MIN_H
    use = None
    if top is not None and (floor or top_z <= TOP_GRASP_MAX_Z):
        use = "top"
    elif side_ok:
        use = "side"
    elif top is not None:
        use = "top_high"
    if use is None:
        if h < 0.014:
            why = f"too thin: {100 * h:.1f} cm high, nothing above the surface for the pads to bite"
        elif g["side_w"] is not None and g["side_w"] > OPEN_GAP:
            why = f"too wide: no part under 8 cm (narrowest silhouette {100 * g['side_w']:.0f} cm) and no rim, neck or strap section the open jaws can come down over"
            if h < 0.03 and not floor:
                why += "; flat on a surface: would need a slide-to-the-edge pinch (no such skill)"
        elif floor:
            why = "no section the open jaws can come down over from above (floor picks are top-down only)"
        else:
            why = f"only {100 * h:.1f} cm high and no top-down section: nothing for the pads"
        return dict(out, verdict="no", approach=None, axis_deg=None, width_cm=None, why=why)
    notes = []
    if use == "side":
        w, ax = g["side_w"], g["side_axis"]; verdict = "yes" if w <= W_YES else "marginal"
        if w > W_YES:
            notes.append(f"{100 * w:.1f} cm across: fits the 7.9 cm open jaws with under 5 mm to spare each side")
        out.update(approach="side-on (hand comes in level, jaws close across it)", axis_deg=round(math.degrees(ax)), width_cm=round(100 * w, 1), pad_height_cm=round(100 * (h / 2), 1))
        if not floor and top is not None:
            notes.append(f"a top-down section also exists ({100 * top['width']:.1f} cm) but its top is {top_z:.2f} m up")
    else:
        w = top["width"]; verdict = "yes"
        out.update(approach="top-down" + (" (rim / wall: one jaw inside, one outside)" if w < 0.012 else ""), axis_deg=round(math.degrees(math.atan2(top["close"][1], top["close"][0])) % 180),
                   width_cm=round(100 * w, 1), pad_height_cm=round(100 * (top["z"] - max(0.0, float(o.plo[2]))), 1), off_centre_cm=round(100 * top["off_centre"], 1), n_sections=len(g["options"]))
        if g["tight"]:
            verdict = "marginal"; notes.append(f"{100 * w:.1f} cm across: fits the 7.9 cm open jaws with under 4.5 mm to spare a side; the floor agent's search (7.0 cm) rejects it today")
        if use == "top_high":
            verdict = "marginal"; notes.append(f"only a top-down section, and its top is {top_z:.2f} m up: the wrist would have to be about {top_z + 0.10:.2f} m high (ASSUMED limit {TOP_GRASP_MAX_Z + 0.10:.2f} m)")
        if top["off_centre"] > 0.08 and (o.mass or 0) >= 0.2:
            verdict = "marginal"; notes.append(f"the section is {100 * top['off_centre']:.0f} cm off the thing's middle: it can swing or tip in the jaws (the light saber slipped out this way in a live run)")
    if (o.mass or 0) > MASS_MARGINAL:
        verdict = "marginal"; notes.append(f"{o.mass:.2f} kg: heavy for pad friction alone (measured squeeze 6 N a pad)")
    out.update(verdict=verdict, why="; ".join(notes) if notes else "a section narrower than 7 cm with pad bite")
    if "the floor agent's search" in out["why"] and verdict == "yes":
        out["verdict"] = "marginal"
    return out


# ---------------------------------------------------------------- v3: the big floor things, moved by carry2 / drag (physics of the pack's own bodies)
HOLD_F_MAX, HOLD_T_MAX = 40.0, 4.0        # N, N m: urc.tasks.home.hold.Hold defaults (f_max, t_max): past these the held thing is pulled out of the hold
G_ACC = 9.81
BIG_METHOD = {"r127i1_scooter": "carry2", "r126i1_scooter": "carry2", "r106i1_umbrella": "drag"}
T_BIG = dict(carry2_take=30.0, carry2_set=20.0, drag_take=25.0, drag_release=10.0, close_door=60.0)   # ASSUMED (basket carry: take ~25 s seen live)


def body_mu(o):
    """Sliding friction against the floor as MuJoCo mixes it (max of the two geoms): the thing's own and the floor's /
    the rug's under it (floor 0.6, rugs and the mat 0.85 in the pack)."""
    bid = m.body(o.id + "_body").id
    mu_o = max(float(m.geom_friction[g][0]) for g in range(m.ngeom) if m.geom_bodyid[g] == bid and (m.geom_contype[g] or m.geom_conaffinity[g]))
    on_rug = any(q.cls == "rug" and np.all(o.c[:2] > q.lo[:2]) and np.all(o.c[:2] < q.hi[:2]) for q in OBJ.values() if q is not o)
    return mu_o, max(mu_o, 0.85 if on_rug else 0.6), ("rug 0.85" if on_rug else "floor 0.6")


def scooter_physics(o):
    """Quasi-static 2-D statics along the deck (by geometry, not verified). The pack's body: one rigid body, its centre
    of mass at the body origin (the middle of its box), no wheel joints: on the floor it SLIDES, it does not roll."""
    bid = m.body(o.id + "_body").id; W = float(m.body_mass[bid]) * G_ACC; com = d.xipos[bid].copy()
    mu_o, mu, under = body_mu(o)
    sides = [c for c in GV2[o.name]["grasps"].get("side", []) if c["verdict"] == "yes"]
    bar_z = max(c["point"][2] for c in sides)                                     # the handlebar: the highest side sections
    P = o.P; top = P[P[:, 2] > bar_z - 0.06]; stem_xy = top[:, :2].mean(0)
    u = com[:2] - stem_xy; u /= np.linalg.norm(u)                                 # along the deck, from the stem to the middle
    w_ax = np.array([-u[1], u[0]]); bar_w = float(np.ptp(top[:, :2] @ w_ax))
    low = P[P[:, 2] < P[:, 2].min() + 0.02]; s = (low[:, :2] - stem_xy) @ u
    s_f, s_r = float(s.min()), float(s.max()); s_c = float((com[:2] - stem_xy) @ u); z_c = float(com[2]); z_h = float(bar_z)
    out = dict(mass_kg=round(W / G_ACC, 2), weight_N=round(W, 1), friction=dict(thing=mu_o, mixed=mu, under=under, rule="MuJoCo takes the larger of the two"),
               com_scene=[round(float(v), 3) for v in com], com_note="the pack puts the centre of mass at the middle of the body's box (0.5 m up), not where a real scooter has it",
               handlebar=dict(z_m=round(z_h, 2), width_m=round(bar_w, 2), stem_scene=[round(float(v), 3) for v in stem_xy], deck_dir=[round(float(v), 3) for v in u]),
               contacts_along_deck_m=[round(s_f, 2), round(s_r, 2)], com_along_deck_m=round(s_c, 3), basis=BASIS)
    # (a) drag UPRIGHT by the handlebar, stem first: both ends slide; the pull at bar height tips it forward about the
    #     leading end unless the hand adds a torque
    F_a = mu * W; tau_a = max(0.0, F_a * z_h - W * (s_c - s_f))
    out["drag_upright"] = dict(hand_force_N=round(F_a, 1), hand_torque_needed_Nm=round(tau_a, 1),
                               verdict="no" if tau_a > HOLD_T_MAX else "yes",
                               why=f"sliding needs {F_a:.1f} N ({mu} x {W:.1f} N); pulled at {z_h:.2f} m it tips onto its front end unless the hand holds {tau_a:.1f} N m (hold limit {HOLD_T_MAX} N m)")
    # (b) drag TILTED on its rear end (front lifted until the front end clears the floor by 5 cm), stem first
    best = None
    for th_deg in range(3, 41):
        th = math.radians(th_deg)
        if (s_r - s_f) * math.sin(th) < 0.05:
            continue
        # coordinates from the rear contact, forward = toward the stem; the body turned about the rear contact, front up
        x_c, zc_ = (s_r - s_c) * math.cos(th) - z_c * math.sin(th), (s_r - s_c) * math.sin(th) + z_c * math.cos(th)
        x_h, zh_ = (s_r - 0.0) * math.cos(th) - z_h * math.sin(th), (s_r - 0.0) * math.sin(th) + z_h * math.cos(th)
        Fz = W * (x_c + mu * zh_) / (x_h + mu * zh_); N = W - Fz; Fx = mu * N
        if N < 0 or Fz < 0:
            continue
        F = math.hypot(Fx, Fz)
        if best is None or F < best[0]:
            best = (F, th_deg, Fz, Fx, N, zh_)
    if best:
        F, th_deg, Fz, Fx, N, zh_ = best
        out["drag_tilted"] = dict(tilt_deg=th_deg, hand_up_N=round(Fz, 1), hand_pull_N=round(Fx, 1), hand_force_N=round(F, 1), rear_end_load_N=round(N, 1), hand_z_m=round(zh_, 2),
                                  verdict="marginal" if F <= HOLD_F_MAX else "no",
                                  why=f"tilted {th_deg} deg onto its rear end: the hand lifts {Fz:.1f} N and pulls {Fx:.1f} N ({F:.1f} N of the {HOLD_F_MAX:.0f} N hold) with no torque, "
                                      f"but it balances on two points (hand + rear end): it can roll about that line, and only the 4 N m hold torque keeps it upright; one hand at the side of the body")
    # (c) carry2: both hands on the handlebar ends, lifted 3 cm; it hangs from the bar
    d_bar = abs(s_c)                                                              # the centre of mass is this far from the bar along the deck
    per_hand_F = W / 2; per_hand_T = W * d_bar / 2
    out["carry2"] = dict(hands="both on the handlebar, " + f"{bar_w - 0.06:.2f} m apart", hand_z_m=round(z_h + 0.03, 2), per_hand_N=round(per_hand_F, 1), per_hand_torque_Nm=round(per_hand_T, 2),
                         verdict="yes" if per_hand_F <= 0.5 * HOLD_F_MAX and per_hand_T <= HOLD_T_MAX else ("marginal" if per_hand_F <= HOLD_F_MAX else "no"),
                         why=f"{per_hand_F:.1f} N a hand ({100 * per_hand_F / HOLD_F_MAX:.0f} % of the hold's {HOLD_F_MAX:.0f} N); the centre of mass is {d_bar:.2f} m off the bar, "
                             f"{per_hand_T:.1f} N m a hand ({100 * per_hand_T / HOLD_T_MAX:.0f} % of the {HOLD_T_MAX} N m hold torque; past it the deck swings down until its far end "
                             f"touches the floor, which turns the carry into a drag, not a drop); the robot carries {W / G_ACC:.1f} kg about {0.33 + d_bar:.2f} m ahead of the pelvis "
                             f"(the 0.3 kg basket already pitched the pelvis 0.13 rad, run 1119_001520)")
    rec = "carry2" if out["carry2"]["verdict"] != "no" else ("drag_tilted" if best and out["drag_tilted"]["verdict"] != "no" else None)
    out["recommended"] = rec
    out["why_recommended"] = ("carry2: the load is split evenly between the hands, nothing balances on a point, the hold limits are not reached (force and torque), it is the same "
                              "take / stand / walk / set down pattern as the toy-basket carry that worked live (run 1118_232318); dragging upright is impossible by physics "
                              f"({tau_a:.1f} N m needed at the hand), and the tilted drag puts {best[2] if best else 0:.0f} N on ONE hand at the side of the body with a roll the hold must stop"
                              if rec == "carry2" else "the tilted drag is the only way inside the hold's limits")
    return out


def umbrella_physics(o):
    """The big open umbrella: in physics a FLAT slab (its one collision hull is 3 cm high; the 20 cm dome is drawn only)."""
    bid = m.body(o.id + "_body").id; W = float(m.body_mass[bid]) * G_ACC
    mu_o, mu, under = body_mu(o)
    L = float(max(o.phi[0] - o.plo[0], o.phi[1] - o.plo[1])); z_h = 0.60
    th = math.asin(min(1.0, z_h / L)); x_h = L * math.cos(th); x_c = x_h / 2
    Fz = W * (x_c + mu * z_h) / (x_h + mu * z_h); N = W - Fz; Fx = mu * N; F = math.hypot(Fz, Fx)
    return dict(mass_kg=round(W / G_ACC, 2), weight_N=round(W, 2), friction=dict(thing=mu_o, mixed=mu, under=under),
                collider=f"one convex hull {100 * (o.phi[0] - o.plo[0]):.0f} x {100 * (o.phi[1] - o.plo[1]):.0f} x {100 * (o.phi[2] - o.plo[2]):.0f} cm (the drawn dome is 20 cm high): there is NO handle in physics",
                drag_by_edge=dict(grip="its rim (side section 5.3-5.8 cm at 2 cm above the floor; deep squat, hand pitched down: marginal)", hand_z_m=z_h, hand_up_N=round(Fz, 1),
                                  hand_pull_N=round(Fx, 1), hand_force_N=round(F, 1), far_edge_load_N=round(N, 1), verdict="marginal",
                                  why=f"near rim lifted to {z_h} m, far rim slides: {F:.1f} N at the hand ({100 * F / HOLD_F_MAX:.0f} % of the hold), no torque to speak of; the grasp at floor level is the hard part"),
                carry_one_hand=dict(verdict="no", why=f"lifted clear it hangs {L:.2f} m below the hand: the hand would need {L + 0.05:.2f} m (pads reach 1.30-1.40 m only with the arm high and a lean) and a 1.1 m disc swinging beside the legs"),
                carry2=dict(verdict="no", why=f"two hands on opposite rims would be {L:.2f} m apart; the arms reach about 0.6 m apart in front"),
                recommended="drag_by_edge", why_recommended="2-3 N at the hand; the only way the jaws can hold it (the handle is not in the collider)", basis=BASIS)


BIG = {}
for n_, meth_ in BIG_METHOD.items():
    o_ = OBJ[n_]
    phys_ = scooter_physics(o_) if meth_ == "carry2" else umbrella_physics(o_)
    BIG[n_] = dict(method=meth_, physics=phys_)


def big_grasp(o):
    b = BIG[o.name]; ph = b["physics"]
    if b["method"] == "carry2":
        c = ph["carry2"]; v = c["verdict"]
        return dict(basis=BASIS, verdict=v, type="carry2", approach="both hands on the handlebar ends (side grasp, jaws horizontal round the 2.7 cm bar)",
                    why=c["why"], width_cm=2.7, skill="NEW: carry2 (two hands, the toy-basket take / set-down pattern: basket_skills.take_basket / set_basket_down)",
                    new_type=True, physics=ph, types={"carry2": v})
    c = ph["drag_by_edge"]
    return dict(basis=BASIS, verdict=c["verdict"], type="drag", approach="one hand on the rim at floor level, stand, drag it with the far rim on the floor",
                why=c["why"], skill="NEW: drag (floor side grasp at the rim, stand up holding, walk; release at the spot)", new_type=True, physics=ph, types={"drag": c["verdict"]})


for o in FREE:
    o.g = grasp_info(o)
    o.grasp_v1 = grasp_verdict_v1(o)
    o.grasp = big_grasp(o) if o.name in BIG else grasp_verdict(o)

# ---------------------------------------------------------------- navigation model (same rules as skills.scene_rects, offline)
FLOOR = OBJ["floor_oak"]
LO, HI, RES = FLOOR.lo[:2].copy(), FLOOR.hi[:2].copy(), 0.05
# the dishwasher: open in the pack (door down, both racks out over it). The OPTIONAL tidy step closes it: racks pushed in,
# door lifted shut. The plan is made with it closed; the open state is kept for the comparison (sink stance etc.)
DW_CLOSED_Q = {"r32i1_door": -math.pi / 2, "r33i1_rack": 0.40, "r33i2_rack": 0.35}
DW_IN_RACKS = [n for n in OBJ if n.startswith(("r65i", "r66i", "r67i"))]        # dishes in the racks go in with them
DW_CLOSE = "--dishwasher-open" not in sys.argv
d_closed = mujoco.MjData(m)
for n_, v_ in DW_CLOSED_Q.items():
    d_closed.qpos[m.jnt_qposadr[m.joint(OBJ[n_].id + "_joint").id]] = v_
mujoco.mj_forward(m, d_closed)


ORIENTED = "--axis-aligned" not in sys.argv


class PolyRect(NAV.Rect):
    """A fixed piece's footprint as its convex outline (the box round it is kept for the coarse uses: c, h, R)."""

    def __init__(self, V2, name):
        from scipy.spatial import ConvexHull
        V2 = np.asarray(V2, float)
        self.V = V2[ConvexHull(V2).vertices]                 # counter-clockwise
        c, h, yaw = NAV.min_rect(V2)
        super().__init__(c, h, yaw, low=False, name=name)

    def dist(self, P):
        P = np.asarray(P, float)[:, :2]
        A = self.V; AB = np.roll(A, -1, axis=0) - A
        AP = P[:, None, :] - A[None]
        t = np.clip((AP * AB[None]).sum(-1) / (AB * AB).sum(-1)[None], 0.0, 1.0)
        dmin = np.linalg.norm(AP - t[..., None] * AB[None], axis=2).min(1)
        inside = np.all(AB[None, :, 0] * AP[..., 1] - AB[None, :, 1] * AP[..., 0] >= 0, axis=1)
        return np.where(inside, 0.0, dmin)


def fixed_rects(dd, oriented=ORIENTED):
    """Footprints of the fixed pieces. v2: a piece that stands askew (the diagonal sink-corner face and its doors) gets
    its own turned rectangle when that is clearly smaller than its axis-aligned box (the room builder's piece_boxes are
    axis-aligned: there a diagonal piece blocks a triangle of floor in front of it)."""
    out = []
    for g_ in range(m.ngeom):
        if not (m.geom_contype[g_] or m.geom_conaffinity[g_]):
            continue
        q = BY_ID.get(m.geom(g_).name[:11])
        if q is None or q.free or q.cls in ("floor", "ceiling"):
            continue
        mid = int(m.geom_dataid[g_]); a = int(m.mesh_vertadr[mid]); n = int(m.mesh_vertnum[mid])
        Vw = m.mesh_vert[a:a + n] @ dd.geom_xmat[g_].reshape(3, 3).T + dd.geom_xpos[g_]
        lo, hi = Vw.min(0), Vw.max(0)
        if lo[2] < 1.2 and hi[2] > 0.03:                      # anything fixed is kept a body radius away, however low
            r = NAV.Rect((lo[:2] + hi[:2]) / 2, (hi[:2] - lo[:2]) / 2, 0.0, low=False, name=q.name)
            if oriented:
                from scipy.spatial import ConvexHull
                try:
                    area = ConvexHull(Vw[:, :2]).volume
                except Exception:
                    area = float(np.prod(hi[:2] - lo[:2]))
                if area < 0.9 * float(np.prod(hi[:2] - lo[:2])):   # askew or cut on the diagonal: its own outline
                    r = PolyRect(Vw[:, :2], q.name)
            r.top = float(hi[2]); r.fixed = True
            out.append(r)
    return out


base_open = fixed_rects(d)
base_closed = fixed_rects(d_closed)
base_closed_aabb = fixed_rects(d_closed, oriented=False)
base_rects = list(base_closed if DW_CLOSE else base_open)
WALK_OVER_THIN = []                                       # paper scraps under 1.2 cm that no grasp can take: the feet may step on them
loose_rects = {}
for o in FREE:
    if o.plo[2] > 0.25 or (o.cls in ("cable", "rug") and o.name not in MOVE) or not len(o.P):     # up on furniture / cords and mats are walked over (v3: the strap is picked, so it has a footprint)
        continue
    if o.cls == "paper" and o.phi[2] - o.plo[2] < 0.012 and o.grasp["verdict"] == "no":
        Pp = o.P[:: len(o.P) // 400 + 1]; c, h, yaw = NAV.min_rect(Pp)
        o.rect = NAV.Rect(c, h, yaw, low=True, name=o.name); o.rect.top = float(o.phi[2]); o.rect.fixed = False
        WALK_OVER_THIN.append(o.name); continue
    if DW_CLOSE and o.name in DW_IN_RACKS:
        Pp = o.P[:: len(o.P) // 400 + 1]; c, h, yaw = NAV.min_rect(Pp)
        o.rect = NAV.Rect(c, h, yaw, low=True, name=o.name); o.rect.top = float(o.phi[2]); o.rect.fixed = False
        base_open.append(o.rect)                          # open: on the pulled-out rack; closed: inside the dishwasher
        continue
    Pp = o.P[:: len(o.P) // 400 + 1]
    c, h, yaw = NAV.min_rect(Pp)
    big = (o.mass or 0) > 1.0 or (max(o.phi[0] - o.plo[0], o.phi[1] - o.plo[1]) > 0.25 and o.phi[2] > 0.12)
    r = NAV.Rect(c, h, yaw, low=not big, name=o.name); r.top = float(o.phi[2]); r.fixed = False
    o.rect = r
    if (o.status == "mess_to_move" and o.grasp["verdict"] != "no") or o.name == "r186i1_basket":
        loose_rects[o.name] = r                             # these go away (or are carried) during the episode
    else:
        base_rects.append(r); base_open.append(r)
bin_rect = NAV.Rect(BIN["xy"], [0.16, 0.16], 0.0, low=False, name="rubbish_bin"); bin_rect.top = 0.40; bin_rect.fixed = False
loose_rects["rubbish_bin"] = bin_rect


# ---------------------------------------------------------------- v3: doors left open, and where the big things go. Chosen BEFORE the walking grid:
# once put down, the placed things are obstacles of the final floor (v2 left everything big where it was).
def _rot(yw):
    c_, s_ = math.cos(yw), math.sin(yw)
    return np.array([[c_, -s_], [s_, c_]])


def body_pts(dd, bid):
    P_ = []
    for g_ in range(m.ngeom):
        if m.geom_bodyid[g_] != bid or not (m.geom_contype[g_] or m.geom_conaffinity[g_]) or m.geom_type[g_] != mujoco.mjtGeom.mjGEOM_MESH:
            continue
        mid = int(m.geom_dataid[g_]); a = int(m.mesh_vertadr[mid]); n = int(m.mesh_vertnum[mid])
        P_.append(m.mesh_vert[a:a + n] @ dd.geom_xmat[g_].reshape(3, 3).T + dd.geom_xpos[g_])
    return np.vstack(P_) if P_ else np.zeros((0, 3))


JOINTS = []
for j_ in range(m.njnt):
    if m.jnt_type[j_] in (mujoco.mjtJoint.mjJNT_HINGE, mujoco.mjtJoint.mjJNT_SLIDE):
        q_ = BY_ID.get(m.body(m.jnt_bodyid[j_]).name[:11])
        if q_ is not None:
            JOINTS.append((j_, q_))
JOINTED = {q_.name for _, q_ in JOINTS}
STATIC_RECTS = [r for r in base_open if getattr(r, "fixed", False) and r.name not in JOINTED]
DOORS, SWING = {}, []
_dd = mujoco.MjData(m)                                       # one scratch MjData (each one holds a 260 MB arena)
for j_, q_ in JOINTS:
    bid_ = int(m.jnt_bodyid[j_]); lo_, hi_ = (float(v) for v in m.jnt_range[j_]); res_ = {}
    for key_, qq in (("pack", 0.0), ("lo", lo_), ("hi", hi_)):
        dd_ = _dd; dd_.qpos[:] = m.qpos0; dd_.qpos[m.jnt_qposadr[j_]] = qq; mujoco.mj_kinematics(m, dd_)
        P_ = body_pts(dd_, bid_)
        if not len(P_):
            break
        P2 = P_[:: max(1, len(P_) // 300), :2]
        near_ = [r for r in STATIC_RECTS if np.linalg.norm(r.c - P2.mean(0)) < 3.0]
        so = float(np.mean(np.min([r.dist(P2) for r in near_], axis=0))) if near_ else 0.0
        res_[key_] = dict(q=qq, lo=P_.min(0), hi=P_.max(0), stick_out=so)
    if len(res_) < 3:
        continue
    ck = min(("lo", "hi"), key=lambda k_: res_[k_]["stick_out"])
    is_open = bool(res_["pack"]["stick_out"] > res_[ck]["stick_out"] + 0.08)
    frames_ = [q for q in OBJ.values() if q.cls == "door_frame"]
    in_frame = [f_ for f_ in frames_ if np.all(res_["pack"]["lo"][:2] > f_.lo[:2] - 0.10) and np.all(res_["pack"]["hi"][:2] < f_.hi[:2] + 0.10)]
    if in_frame:                                             # a room door standing in its frame (the walls carry no object id, so the distance test cannot see them)
        is_open = False; ck = "pack" if abs(lo_) < 1e-6 or abs(hi_) < 1e-6 else ck
    lo_all = np.min([r_["lo"] for r_ in res_.values()], axis=0); hi_all = np.max([r_["hi"] for r_ in res_.values()], axis=0)
    DOORS[q_.name] = dict(joint=q_.id + "_joint", kind="hinge" if m.jnt_type[j_] == mujoco.mjtJoint.mjJNT_HINGE else "slide", range=[round(lo_, 3), round(hi_, 3)],
                          q_in_pack=0.0, q_closed=round(res_[ck]["q"], 3), open_in_pack=is_open, mass_kg=round(float(m.body_mass[bid_]), 2),
                          damping=round(float(m.dof_damping[m.jnt_dofadr[j_]]), 2), hinge_or_axis_scene=[round(float(v), 3) for v in d.xanchor[j_]], axis=[round(float(v), 2) for v in d.xaxis[j_]],
                          sticks_out_m=dict(pack=round(res_["pack"]["stick_out"], 2), closed=round(res_[ck]["stick_out"], 2)),
                          box_pack_scene=[[round(float(v), 2) for v in res_["pack"]["lo"]], [round(float(v), 2) for v in res_["pack"]["hi"]]],
                          box_closed_scene=[[round(float(v), 2) for v in res_[ck]["lo"]], [round(float(v), 2) for v in res_[ck]["hi"]]], basis=BASIS)
    SWING.append((lo_all[:2], hi_all[:2], q_.name, float(lo_all[2])))
OPEN_DOORS = [n for n, v in DOORS.items() if v["open_in_pack"]]
FRONT_DOOR = "r11i1_leaf"
FRONT_DOOR_XY = np.array([4.63, -2.30])                   # the middle of the front door's opening (frame r11i1, scene)
PLACED, V3_SPOT, V3_SEARCH = [], {}, {}


def fp_points(c, h, yw, step=0.03):
    xs = np.linspace(-h[0], h[0], max(2, int(2 * h[0] / step) + 1)); ys = np.linspace(-h[1], h[1], max(2, int(2 * h[1] / step) + 1))
    G_ = np.stack(np.meshgrid(xs, ys, indexing="ij"), -1).reshape(-1, 2)
    return np.asarray(c, float)[:2] + G_ @ _rot(yw).T


def spot_clear(c, h, yw, margin=0.03, z_top=1.0, extra_avoid=()):
    """Footprint (centre c, half sizes h, yaw) free of everything that stays (fixed pieces, loose things not moved, things
    placed before), of the floor any door / drawer sweeps, and inside the floor."""
    P_ = fp_points(c, h, yw)
    if np.any(P_ < LO + 0.05) or np.any(P_ > HI - 0.05):
        return False, "outside the floor"
    for r in base_rects + PLACED:
        if np.linalg.norm(r.c - np.asarray(c)[:2]) - np.linalg.norm(r.h) - np.linalg.norm(h) > 0.2:
            continue
        if float(r.dist(P_).min()) < margin:
            return False, r.name
    for lo_, hi_, nm_, zlo_ in SWING:
        if zlo_ < z_top and np.any(np.all((P_ > lo_ - margin) & (P_ < hi_ + margin), axis=1)):
            return False, "the swing of " + nm_
    for lo_, hi_, nm_ in tuple(extra_avoid) + KEEP_FREE:
        if np.any(np.all((P_ > lo_) & (P_ < hi_), axis=1)):
            return False, nm_
    return True, None


KEEP_FREE = ((OBJ["r119i1_mat"].lo[:2] - 0.03, OBJ["r119i1_mat"].hi[:2] + 0.03, "the doormat (the shoes' place)"),)


def touching(c, h, yw, gap=0.07):
    """Fixed things (walls' baseboards, furniture) within `gap` of the footprint: it stands against them."""
    P_ = fp_points(c, h, yw, step=0.05)
    return sorted({r.name for r in base_rects + PLACED if getattr(r, "fixed", False) and np.linalg.norm(r.c - np.asarray(c)[:2]) < 3 and float(r.dist(P_).min()) < gap})


KEY_PTS = {"start": START, "doormat": np.array([2.42, -1.30]), "hamper": np.array([-1.25, -0.95]), "toy basket": np.array([-4.28, -0.45]), "bin": np.array([1.00, 1.45]),
           "sink": np.array([4.45, 1.35]), "tray table": np.array([2.47, 1.60]), "island south": np.array([2.70, -0.35]), "living room": np.array([-2.20, -0.05]),
           "entry (east of the stroller)": np.array([4.30, -1.20]), "hall south": np.array([1.00, -1.40])}
_S3 = np.ones((3, 3), bool)


def _walk_pairs(clear):
    """Walking distance between every two KEY_PTS on a floor whose clearance is `clear` (inf: cut off)."""
    ok = clear > 0
    nx_, ny_ = ok.shape
    idx_ = -np.ones(ok.shape, int); cells_ = np.argwhere(ok); idx_[ok] = np.arange(len(cells_))
    rr, cc, ww = [], [], []
    for dx, dy, w in ((1, 0, 1.0), (0, 1, 1.0), (1, 1, 1.4142), (1, -1, 1.4142)):
        a = idx_[max(0, -dx):nx_ - max(0, dx), max(0, -dy):ny_ - max(0, dy)]
        b = idx_[max(0, dx):nx_ - max(0, -dx), max(0, dy):ny_ - max(0, -dy)]
        k_ = (a >= 0) & (b >= 0); rr.append(a[k_]); cc.append(b[k_]); ww.append(np.full(int(k_.sum()), w * RES))
    Gm = coo_matrix((np.concatenate(ww), (np.concatenate(rr), np.concatenate(cc))), shape=(len(cells_), len(cells_))).tocsr()
    pts_ = LO + cells_ * RES
    src = [int(np.argmin(np.linalg.norm(pts_ - p, axis=1))) for p in KEY_PTS.values()]
    D_ = dijkstra(Gm, directed=False, indices=src)
    return D_[:, src]


G_PRE = NAV.Grid(LO, HI, base_rects, res=RES, r_body=R_BODY, r_foot=R_FOOT)
_XS, _YS = np.meshgrid(LO[0] + np.arange(G_PRE.nx) * RES, LO[1] + np.arange(G_PRE.ny) * RES, indexing="ij")
_PG = np.stack([_XS.ravel(), _YS.ravel()], 1)
CLEAR_PRE = G_PRE.clear.copy()
WALK0 = _walk_pairs(CLEAR_PRE)


def body_yaw0(o):
    R0 = d.xmat[m.body(o.id + "_body").id].reshape(3, 3)
    return math.atan2(R0[1, 0], R0[0, 0])


def place(o, c, h, rect_yaw, low, why, flip=False, z=None):
    """Record a chosen place: the footprint becomes an obstacle of the final floor; the body's target pose (the body
    keeps its pose relative to its footprint; `flip` turns it half round inside the same footprint) is kept."""
    global CLEAR_PRE
    r = NAV.Rect(c, h, rect_yaw, low=low, name=o.name + "@v3"); r.top = float(o.phi[2] - o.plo[2]); r.fixed = False
    PLACED.append(r)
    CLEAR_PRE = np.minimum(CLEAR_PRE, (r.dist(_PG) - (R_FOOT if low else R_BODY)).reshape(CLEAR_PRE.shape))
    bid = m.body(o.id + "_body").id; bp = d.xpos[bid]
    dyaw = rect_yaw - o.rect.yaw + (math.pi if flip else 0.0)
    tgt = np.asarray(c, float)[:2] + _rot(dyaw) @ (bp[:2] - o.rect.c)
    byaw = (body_yaw0(o) + dyaw + math.pi) % (2 * math.pi) - math.pi
    zt = float(bp[2] - o.plo[2]) if z is None else z                       # standing on the floor as it stands now
    V3_SPOT[o.name] = dict(xy=tgt, z=round(zt, 3), yaw_deg=round(math.degrees(byaw), 1), turn_deg=round(math.degrees(dyaw), 1),
                           footprint=dict(c=[round(float(v), 3) for v in c], h=[round(float(v), 3) for v in h], yaw_deg=round(math.degrees(rect_yaw), 1)),
                           note=why, against=touching(c, h, rect_yaw))
    return tgt, dyaw


def search_spot(o, anchor_fn, region, yaws=(0.0, math.pi / 2), step=0.05, need_touch=True, k_eval=30, impact_w=1.0, extra_avoid=(), label=""):
    """Best place for o's footprint in region ((x0, x1), (y0, y1)): clear (spot_clear), against something fixed if
    need_touch, smallest  anchor cost + impact_w * mean extra walking metres between the key points."""
    h = o.rect.h.copy(); cands = []
    for yw in yaws:
        for x in np.arange(region[0][0], region[0][1] + 1e-9, step):
            for y in np.arange(region[1][0], region[1][1] + 1e-9, step):
                ok, _ = spot_clear((x, y), h, yw, extra_avoid=extra_avoid)
                if not ok:
                    continue
                t_ = touching((x, y), h, yw)
                if need_touch and not t_:
                    continue
                cands.append((anchor_fn(np.array([x, y]), h, yw) + (0.0 if t_ else 0.5), x, y, yw, t_))
    cands.sort(key=lambda c_: c_[0]); best = None; tried = []
    base_ = _walk_pairs(CLEAR_PRE)
    for cst, x, y, yw, t_ in cands[:k_eval]:
        r = NAV.Rect((x, y), h, yw, low=o.rect.low, name="cand")
        cl = np.minimum(CLEAR_PRE, (r.dist(_PG) - (R_FOOT if o.rect.low else R_BODY)).reshape(CLEAR_PRE.shape))
        W_ = _walk_pairs(cl)
        fin = np.isfinite(base_)
        cut = int(np.sum(fin & ~np.isfinite(W_))) // 2
        inc = float(np.nanmean(np.where(fin & np.isfinite(W_), W_ - base_, np.nan)))
        tot = cst + impact_w * inc + (100.0 if cut else 0.0)
        tried.append((tot, x, y, yw, t_, inc, cut, base_))
        if best is None or tot < best[0]:
            best = (tot, x, y, yw, t_, inc, cut)
    V3_SEARCH[o.name] = dict(label=label, candidates_clear=len(cands), evaluated=len(tried),
                             best=None if best is None else dict(cost=round(best[0], 2), centre=[round(best[1], 2), round(best[2], 2)], rect_yaw_deg=round(math.degrees(best[3])),
                                                                 against=best[4], extra_walk_m_mean_per_pair=round(best[5], 3), pairs_cut=best[6]),
                             runner_up=[dict(centre=[round(t[1], 2), round(t[2], 2)], cost=round(t[0], 2), extra_walk_m=round(t[5], 3)) for t in sorted(tried)[1:4]])
    return best


# (1) the two scooters: parked upright, nose to a wall, stem out, beside the toy bike (the bike already stands along the hall wall)
bike = OBJ["r128i1_bike"]
for n_ in ("r127i1_scooter", "r126i1_scooter"):
    o_ = OBJ[n_]; ph_ = BIG[n_]["physics"]; stem_ = np.array(ph_["handlebar"]["stem_scene"])
    u_ = np.array(ph_["handlebar"]["deck_dir"], float); u_ /= np.linalg.norm(u_); w_ = np.array([-u_[1], u_[0]])
    su_, sw_ = (o_.P[:, :2] - stem_) @ u_, (o_.P[:, :2] - stem_) @ w_          # its footprint in its own axes (deck along x)
    o_.rect = NAV.Rect(stem_ + u_ * (su_.min() + su_.max()) / 2 + w_ * (sw_.min() + sw_.max()) / 2, [np.ptp(su_) / 2, np.ptp(sw_) / 2], math.atan2(u_[1], u_[0]), low=False, name=n_)
    o_.rect.top = float(o_.phi[2]); o_.rect.fixed = False; loose_rects[n_] = o_.rect
    # packed along the hall wall east of the bike / robot vacuum: deck across the wall, nose 3-6 cm off the baseboard,
    # 2 cm between neighbours; the west-most place that is clear (1 cm steps)
    b_ = None
    for y_ in np.arange(-2.40 + 0.03 + o_.rect.h[0], -2.40 + 0.10 + o_.rect.h[0], 0.01):
        xs_ok = [x_ for x_ in np.arange(0.30, 1.80, 0.01) if spot_clear((x_, y_), o_.rect.h, math.pi / 2, margin=0.02)[0]]
        if xs_ok:
            x_ = xs_ok[0]; t_ = touching((x_, y_), o_.rect.h, math.pi / 2)
            if any("baseboard" in t or "wall" in t for t in t_):
                b_ = (0.0, float(x_), float(y_), math.pi / 2, t_, 0.0, 0); break
    if b_ is not None:
        r_ = NAV.Rect((b_[1], b_[2]), o_.rect.h, b_[3], low=False, name="cand")
        W_ = _walk_pairs(np.minimum(CLEAR_PRE, (r_.dist(_PG) - R_BODY).reshape(CLEAR_PRE.shape))); B_ = _walk_pairs(CLEAR_PRE); f_ = np.isfinite(B_)
        b_ = b_[:5] + (float(np.nanmean(np.where(f_ & np.isfinite(W_), W_ - B_, np.nan))), int(np.sum(f_ & ~np.isfinite(W_))) // 2)
        V3_SEARCH[n_] = dict(label="vehicle corner: packed along the hall wall east of the bike (1 cm steps)", best=dict(centre=[round(b_[1], 2), round(b_[2], 2)], against=b_[4],
                             extra_walk_m_mean_per_pair=round(b_[5], 3), pairs_cut=b_[6]))
    else:
        near_bike = lambda p, h, yw: float(np.linalg.norm(p - bike.c[:2])) + 0.3 * float(np.linalg.norm(p - FRONT_DOOR_XY)) / 4.0
        b_ = search_spot(o_, near_bike, ((-1.5, 3.5), (-2.4, -0.6)), yaws=(math.pi / 2, 0.0), step=0.04, label="vehicle corner (no room left along the hall wall)")
    if b_ is None:
        continue
    _, x_, y_, yw_, t_, inc_, cut_ = b_
    # which way round: the stem (handlebar) at the end AWAY from the wall it stands against
    opts = []
    for flip_ in (False, True):
        dyaw_ = yw_ - o_.rect.yaw + (math.pi if flip_ else 0.0)
        stem_t = np.array([x_, y_]) + _rot(dyaw_) @ (stem_ - o_.rect.c)
        dwall = min((float(r.dist(stem_t[None])[0]) for r in base_rects if r.name in t_), default=9.0)
        opts.append((dwall, flip_, stem_t))
    dwall, flip_, stem_t = max(opts, key=lambda t: t[0])
    place(o_, (x_, y_), o_.rect.h, yw_, False, f"parked upright, nose to {', '.join(t_[:2]) or 'the wall'}, stem and handlebar out ({dwall:.2f} m from it), in the vehicle corner by the toy bike", flip=flip_)
    V3_SPOT[n_]["stem_target_scene"] = [round(float(v), 3) for v in stem_t]
# (2) the big open umbrella: flat, by the entry, clear of the front door's swing and of the walking routes
o_ = OBJ["r106i1_umbrella"]
# by the entry first (cost: distance to the front door + 2 x the mean extra walking per key pair); whole floor as the
# comparison (door distance weighs 0.3 there): the 1.10 x 0.96 m disc may have no place by the door that blocks nothing
b_door = search_spot(o_, lambda p, h, yw: float(np.linalg.norm(p - FRONT_DOOR_XY)), ((1.5, 5.3), (-2.4, 0.3)), yaws=(0.0, math.pi / 2), step=0.05, label="by the entry", impact_w=2.0)
S_door = V3_SEARCH.pop("r106i1_umbrella", None)
_on_wall = lambda p, h, yw: 0.05 * float(np.linalg.norm(p - FRONT_DOOR_XY)) + (0.0 if any("baseboard" in t or "wall" in t for t in touching(p, h, yw)) else 0.6)
b_any = search_spot(o_, _on_wall, ((-5.3, 5.3), (-2.4, 2.3)), yaws=(0.0, math.pi / 2), step=0.15, k_eval=40, label="anywhere, against a wall", impact_w=3.0)
S_any = V3_SEARCH.pop("r106i1_umbrella", None)
V3_SEARCH["r106i1_umbrella"] = dict(by_the_entry=S_door, anywhere=S_any)
UMB_CHOICE = None
if b_door is not None and (b_any is None or b_door[5] <= 0.15 or b_door[5] <= b_any[5] + 0.10):
    b_, UMB_CHOICE = b_door, "by the entry"
elif b_any is not None:
    b_, UMB_CHOICE = b_any, "the least walking cost anywhere (no place by the entry blocks nothing)"
if UMB_CHOICE:
    place(o_, (b_[1], b_[2]), o_.rect.h, b_[3], True, f"lying open (it cannot be closed), against {', '.join(b_[4][:2])}; {np.linalg.norm(np.array(b_[1:3]) - FRONT_DOOR_XY):.2f} m from the front door's opening, "
                                                   f"outside every door's swing; chosen: {UMB_CHOICE}; it adds {b_[5]:.2f} m of walking per key pair on average")
# (3) the small umbrella: by the entry
o_ = OBJ["r107i1_umbrella"]
b_ = search_spot(o_, lambda p, h, yw: float(np.linalg.norm(p - FRONT_DOOR_XY)), ((1.5, 5.3), (-2.4, 0.3)), yaws=(0.0, math.pi / 2), step=0.04, label="by the entry", impact_w=2.0)
if b_ is not None:
    place(o_, (b_[1], b_[2]), o_.rect.h, b_[3], True, f"lying along {', '.join(b_[4][:2])}, {np.linalg.norm(np.array(b_[1:3]) - FRONT_DOOR_XY):.2f} m from the front door's opening")
# (4) the tote from the island: standing on the floor beside the other bags (it stands on the island the same way up)
o_ = OBJ["r70i1_tote"]
BAG_ROW = [q for q in FREE if q.cls == "bag" and q.rest["type"] == "floor" and q.status not in ("mess_to_move",) and q.c[0] > 0.0 and hasattr(q, "rect")]
_c, _h, _y = NAV.min_rect(o_.P[:: len(o_.P) // 400 + 1])
o_.rect = NAV.Rect(_c, _h, _y, low=False, name=o_.name); o_.rect.top = float(o_.phi[2] - o_.plo[2])
b_ = search_spot(o_, lambda p, h, yw: min(float(q.rect.dist(p[None])[0]) for q in BAG_ROW) + 0.15 * float(np.linalg.norm(p - FRONT_DOOR_XY)),
                 ((1.0, 5.3), (-2.4, 0.0)), yaws=(_y, _y + math.pi / 2), step=0.04, label="with the bags", impact_w=2.0)
if b_ is not None:
    nb_ = min(BAG_ROW, key=lambda q: float(q.rect.dist(np.array([b_[1:3]]))[0]))
    place(o_, (b_[1], b_[2]), _h, b_[3], False, f"standing beside {nb_.name}, against {', '.join(b_[4][:2])}")
# (5) the cardboard box: square against the nearest wall, as near as it is now
o_ = OBJ["r175i1_cardboard_box"]
b_ = search_spot(o_, lambda p, h, yw: float(np.linalg.norm(p - OBJ['r175i1_cardboard_box'].c[:2])), ((o_.c[0] - 0.8, o_.c[0] + 0.8), (o_.c[1] - 0.8, o_.c[1] + 0.6)),
                 yaws=(o_.rect.yaw,), step=0.02, label="against the wall", impact_w=2.0)
if b_ is not None:
    place(o_, (b_[1], b_[2]), o_.rect.h, b_[3], False, f"square against {', '.join(b_[4][:2])}, {np.linalg.norm(np.array(b_[1:3]) - o_.c[:2]):.2f} m from where it stands")
for r in PLACED:
    base_rects.append(r); base_open.append(r); base_closed.append(r); base_closed_aabb.append(r)
del _dd
if "--spots-only" in sys.argv:                                 # debugging the v3 places: print and stop (nothing written)
    print("OPEN DOORS", OPEN_DOORS)
    for k_, v_ in DOORS.items():
        print("  door", k_, v_["kind"], "open" if v_["open_in_pack"] else "closed", v_["sticks_out_m"], "q_closed", v_["q_closed"])
    for k_, v_ in V3_SPOT.items():
        print("SPOT", k_, np.round(v_["xy"], 3).tolist(), v_["yaw_deg"], v_["note"], V3_SEARCH.get(k_, {}).get("best"))
    for n_, b_ in BIG.items():
        print("BIG", n_, json.dumps(b_["physics"], default=str)[:1800])
    print(f"{time.time() - T0:.1f} s"); sys.exit(0)
G0 = NAV.Grid(LO, HI, base_rects, res=RES, r_body=R_BODY, r_foot=R_FOOT)
G0_OPEN = NAV.Grid(LO, HI, base_open, res=RES, r_body=R_BODY, r_foot=R_FOOT)       # dishwasher open (the pack as it is)
NX, NY = int(G0.nx), int(G0.ny)
XS, YS = np.meshgrid(LO[0] + np.arange(NX) * RES, LO[1] + np.arange(NY) * RES, indexing="ij")
PG = np.stack([XS.ravel(), YS.ravel()], 1)
loose_clear = {n: (r.dist(PG) - (R_FOOT if r.low else R_BODY)).reshape(NX, NY) for n, r in loose_rects.items()}
S3 = np.ones((3, 3), bool)


def cell(p):
    i = np.clip(np.round((np.asarray(p, float)[:2] - LO) / RES).astype(int), 0, [NX - 1, NY - 1])
    return int(i[0]), int(i[1])


_STATE = {}


def state(ignore=frozenset()):
    """The floor as it is with the things in `ignore` gone: clearance grid, the cells joined to the start, the cells
    where the pelvis may stand (up to 6 cm inside an inflated edge and within 0.25 m of a walkable cell, as Grid.reach_cost)."""
    ignore = frozenset(ignore)
    if ignore not in _STATE:
        clear = G0.clear.copy()
        for n, a in loose_clear.items():
            if n not in ignore:
                clear = np.minimum(clear, a)
        lab, _ = ndimage.label(clear > 0, structure=S3)
        i, j = cell(START)
        if lab[i, j] == 0:
            dd = np.where(lab > 0, np.hypot(XS - START[0], YS - START[1]), np.inf); i, j = np.unravel_index(np.argmin(dd), dd.shape)
        main = lab == lab[i, j]
        stand = ndimage.binary_dilation(main, structure=S3, iterations=5) & (clear > -0.06)
        if len(_STATE) > 400:
            _STATE.clear()
        _STATE[ignore] = dict(clear=clear, main=main, stand=stand, ignore=ignore)
    return _STATE[ignore]


ALL_MOVED = frozenset(loose_rects)                         # the floor after everything planned has been moved (containers lifted too)
ALL_RECTS = base_rects + list(loose_rects.values())
RC = np.array([r.c for r in ALL_RECTS]); RR = np.array([float(np.linalg.norm(r.h)) for r in ALL_RECTS])


def near_rects(p, rad=1.1):
    k = np.where(np.linalg.norm(RC - np.asarray(p)[:2], axis=1) - RR < rad)[0]
    return [ALL_RECTS[i] for i in k]


def R2(yw):
    c, s = math.cos(yw), math.sin(yw)
    return np.array([[c, -s], [s, c]])


def knees_clear(rects, b, yw, gap=0.12, tall=0.15):
    for ky in (0.15, -0.15):
        q = b + R2(yw) @ np.array([0.24, ky])
        for r in rects:
            if r.top > tall and float(r.dist(q[None])[0]) < gap:
                return False, r.name
    return True, None


def feet_clear(b, yw, rects, margin=0.04):
    Rm = R2(yw)
    P = np.array([b + Rm @ np.array([x, sg * y]) for sg in (1, -1) for x in np.linspace(FOOT_X[0], FOOT_X[1], 6) for y in (FOOT_Y[0], (FOOT_Y[0] + FOOT_Y[1]) / 2, FOOT_Y[1])])
    for r in rects:
        if float(r.dist(P).min()) <= margin:
            return False, r.name
    return True, None


H12 = [k * math.pi / 6 for k in range(12)]


def squat_stances(points_heads, own, ignore, x_rel=X_REL, y_rel=Y_REL):
    """Pick / put-down stances for a floor point (as skills.stance_for with squat=True). Returns (stances, why_not)."""
    S = state(ignore); out = []; why = collections.Counter()
    for p, heads in points_heads:
        near = [r for r in near_rects(p) if r.name not in ignore]
        low = [r for r in near if r.low] + ([own] if own is not None else [])
        for side, sg in (("left", 1.0), ("right", -1.0)):
            for yw in (heads if heads is not None else H12):
                b = np.asarray(p, float)[:2] - R2(yw) @ np.array([x_rel, sg * y_rel])
                if np.any(b < LO) or np.any(b > HI) or not S["stand"][cell(b)]:
                    c = S["clear"][cell(b)] if np.all(b >= LO) and np.all(b <= HI) else -1
                    if c <= -0.06:                         # which thing is the pelvis too near to
                        dn = [(float(r.dist(b[None])[0]) - (R_FOOT if r.low else R_BODY), r.name) for r in near]
                        why[min(dn)[1] if dn else "wall"] += 1
                    else:
                        why["no way there (cut off)"] += 1
                    continue
                ok, who = knees_clear(near, b, yw)
                if not ok:
                    why[who] += 1; continue
                ok, who = feet_clear(b, yw, low)
                if not ok:
                    why[who] += 1; continue
                pre = any(S["clear"][cell(b - R2(yw) @ np.array([bk, 0.0]))] > 0 for bk in (0.30, 0.22, 0.15))
                out.append(dict(xy=b, yaw=yw, side=side, pre=pre, room=float(S["clear"][cell(b)]), point=np.asarray(p, float)[:2]))
    out.sort(key=lambda s: (not s["pre"], -s["room"]))
    return out, why


def pick_points(o):
    """Grasp points and the headings they allow for a floor pick."""
    if o.name in CLOTH:
        r = o.rect
        if max(r.h) > 0.08:                               # a garment is taken at an edge (the feet stay off it): the middles of its four sides, 3 cm in
            pts = [r.c + r.R @ (np.array(e, float) * np.maximum(r.h - 0.03, 0.0)) for e in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            return [(p, None) for p in pts]
        return [(r.c, None)]
    return [p for p, _ in pick_points_typed(o)]


def pick_points_typed(o, types=None):
    """[((point xy, headings), (type, candidate, verdict, notes))] for the usable grasps of a floor thing, best first."""
    out = []
    U = sorted(usable(o), key=lambda r: (r[2] != "yes", type_rank(o, r[0]), r[1]["score"]))
    for r in U:
        t, c = r[0], r[1]
        if types and t not in types:
            continue
        if t == "side":
            heads = None                                   # the hand comes in level; any body heading (not measured)
        else:
            a = math.atan2(c["close"][1], c["close"][0]); heads = [a + math.pi / 2, a - math.pi / 2]
        out.append(((np.asarray(c["point"][:2], float), heads), r))
    return out


def floor_reach(o):
    """Is there a pick stance now (trying the grasp types best first); if not, which movable neighbours must go first,
    or which fixed thing blocks."""
    res = dict(basis=BASIS, method="pick stance as skills.stance_for (pelvis 0.28 m from furniture, 0.16 m from small things, knees and feet clear)")
    own = o.rect
    if o.name in CLOTH:
        typed = [(p, ("cloth", None, "yes", [])) for p in pick_points(o)]
    else:
        typed = pick_points_typed(o)
    if not typed:
        typed = [((o.rect.c, None), (None, None, "no", []))]
    key = lambda p: (round(float(p[0]), 3), round(float(p[1]), 3))
    by_pt = {key(p[0]): r for p, r in typed}
    pts = [p for p, _ in typed]
    o.grasp_used = None
    # best type first: a type that has a stance now; a better type that only needs neighbours cleared first is kept
    # before a worse type that works now (the route clears the neighbours first)
    types_ = list(dict.fromkeys(r[0] for _, r in typed))
    for t in types_:
        st_t, _ = squat_stances([p for p, r in typed if r[0] == t], own, {o.name})
        if st_t:
            s = st_t[0]; o.grasp_used = by_pt.get(key(s["point"]))
            return dict(res, verdict="yes", stance=[round(float(s["xy"][0]), 2), round(float(s["xy"][1]), 2), round(math.degrees(s["yaw"]))], hand=s["side"],
                        walk_in_from_behind=bool(s["pre"]), n_stances=len(st_t), clear_first=[], grasp_type=t), s
        st_all, _ = squat_stances([p for p, r in typed if r[0] == t], own, ALL_MOVED | {o.name})
        if st_all:
            pts = [p for p, r in typed if r[0] == t]          # this type works once neighbours are gone: use it (below)
            break
    st, why = squat_stances(pts, own, {o.name})
    st2, why2 = squat_stances(pts, own, ALL_MOVED | {o.name})
    if not st2:
        top = [k for k, _ in why2.most_common(3)]
        return dict(res, verdict="no", stance=None, hand=None, clear_first=[], blocked_by=top,
                    why="no pick stance even with every movable thing gone: blocked by " + ", ".join(top)), None
    nb = sorted((float(np.linalg.norm(r.c - o.rect.c)), n) for n, r in loose_rects.items() if n != o.name and np.linalg.norm(r.c - o.rect.c) < 1.3)
    nb = [n for _, n in nb][:7]
    for k in (1, 2, 3):
        for combo in itertools.combinations(nb, k):
            st3, _ = squat_stances(pts, own, set(combo) | {o.name})
            if st3:
                s = st3[0]; o.grasp_used = by_pt.get(key(s["point"]))
                return dict(res, verdict="after clearing", stance=[round(float(s["xy"][0]), 2), round(float(s["xy"][1]), 2), round(math.degrees(s["yaw"]))], hand=s["side"],
                            walk_in_from_behind=bool(s["pre"]), clear_first=list(combo), blocked_by=[k_ for k_, _ in why.most_common(3)],
                            why="no stance now (in the way: " + ", ".join(k_ for k_, _ in why.most_common(3)) + "); a stance appears once " + ", ".join(combo) + " is gone"), s
    s = st2[0]; o.grasp_used = by_pt.get(key(s["point"]))
    return dict(res, verdict="after clearing", stance=[round(float(s["xy"][0]), 2), round(float(s["xy"][1]), 2), round(math.degrees(s["yaw"]))], hand=s["side"],
                walk_in_from_behind=bool(s["pre"]), clear_first=nb, blocked_by=[k_ for k_, _ in why.most_common(3)],
                why="no stance now; one appears only when most of the neighbours are gone: " + ", ".join(nb)), s


def nearest_stand(xy, ignore, rmax=1.5):
    S = state(ignore)
    dd = np.where(S["stand"], np.hypot(XS - xy[0], YS - xy[1]), np.inf)
    i, j = np.unravel_index(np.argmin(dd), dd.shape)
    return (np.array([XS[i, j], YS[i, j]]), float(dd[i, j])) if dd[i, j] < rmax else (None, float("inf"))


def reach_verdict(dist, z):
    if z > 1.25:
        return "no", f"{z:.2f} m up: above the G1's reach"
    ry, rm, src = reach_limits(z)
    if dist <= ry:
        v, w = "yes", f"the pelvis can stand {dist:.2f} m from it"
    elif dist <= rm:
        v, w = "marginal", f"nearest standing place is {dist:.2f} m from it: needs a trunk lean over the furniture ({src} limit {ry:.2f} m without)"
    else:
        return "no", f"nearest standing place is {dist:.2f} m from it ({src} reach {rm:.2f} m at most)"
    if z < 0.35 and z > 0.04:
        v, w = "marginal", w + "; low shelf: deep squat and a level reach into the cubby"
    if z > 1.05:
        v, w = "marginal", w + f"; grasp height about {z:.2f} m: at or above the shoulder"
    return v, w


def nearest_stand_dir(xy, ignore, approach=None, max_angle=60.0, rmax=1.5):
    """Nearest standing cell to xy; with `approach` (unit xy, the direction the hand moves in at the end) only cells the
    hand can come from: the cell lies behind the target, within max_angle of -approach."""
    S = state(ignore)
    dx, dy = XS - xy[0], YS - xy[1]
    dd = np.hypot(dx, dy)
    ok = S["stand"]
    if approach is not None:
        cosang = -(dx * approach[0] + dy * approach[1]) / np.maximum(dd, 1e-9)
        ok = ok & (cosang >= math.cos(math.radians(max_angle)))
    dd = np.where(ok, dd, np.inf)
    i, j = np.unravel_index(np.argmin(dd), dd.shape)
    return (np.array([XS[i, j], YS[i, j]]), float(dd[i, j])) if dd[i, j] < rmax else (None, float("inf"))


def slide_blockers(o, c):
    """Things on the same support in the way of an edge grasp's slide (xy boxes swept along the slide)."""
    if c.get("slide_m", 0.0) <= 0.0:
        return []
    out_dir = -np.asarray(c["approach"][:2], float)
    lo, hi = o.plo[:2].copy(), o.phi[:2].copy()
    lo2, hi2 = np.minimum(lo, lo + out_dir * c["slide_m"]), np.maximum(hi, hi + out_dir * c["slide_m"])
    blk = []
    for q in FREE:
        if q is o or q.rest.get("support") != o.rest.get("support"):
            continue
        if np.all(q.plo[:2] < hi2 - 0.005) and np.all(q.phi[:2] > lo2 + 0.005) and not (np.all(q.plo[:2] < hi - 0.005) and np.all(q.phi[:2] > lo + 0.005)):
            blk.append(q.name)
    return blk


def surface_reach(o):
    """A thing on furniture, per usable grasp candidate: the nearest place the pelvis may stand from which the hand can
    come in the candidate's way (side and edge grasps from their own side), now / with the movable things gone. The
    best candidate by (reach, grasp verdict, type order) is used."""
    rank = {"yes": 0, "after clearing": 1, "marginal": 2, "no": 3}
    best = None
    U = usable(o) if o.name not in CLOTH else []
    if not U:
        U = [(None, dict(point=[float(o.c[0]), float(o.c[1]), float(o.plo[2] + min(0.5 * (o.phi[2] - o.plo[2]), 0.12))], approach=[0, 0, -1], score=0.0), o.grasp.get("verdict", "no"), [])]
    for (t, c, gv, notes) in U:
        xy = np.asarray(c["point"][:2], float); zg = float(c["point"][2])
        app = None
        if t in ("side", "edge"):
            a = np.asarray(c["approach"][:2], float); app = a / max(np.linalg.norm(a), 1e-9)
        blk_slide = slide_blockers(o, c) if t == "edge" else []
        b0, d0 = nearest_stand_dir(xy, set(), app); v0, w0 = reach_verdict(d0, zg)
        b1, d1 = nearest_stand_dir(xy, ALL_MOVED, app); v1, w1 = reach_verdict(d1, zg)
        if blk_slide:
            stay = [n for n in blk_slide if n not in loose_rects and not (OBJ[n].status == "mess_to_move")]
            if stay:
                continue                                     # something that stays is in the slide's way
        if rank[v1] < rank[v0] or blk_slide:
            if b1 is None:
                continue
            i, j = cell(b1)
            blk = [n for n, a_ in loose_clear.items() if a_[i, j] <= -0.06 or not state(ALL_MOVED - {n})["stand"][i, j]] + blk_slide
            r_ = dict(verdict="after clearing" if v1 == "yes" else v1, stand_at=[round(float(b1[0]), 2), round(float(b1[1]), 2)], stand_dist_m=round(d1, 2),
                      grasp_height_m=round(zg, 2), clear_first=sorted(set(blk)), why=f"now: {w0}. With {', '.join(sorted(set(blk))) or 'the movable things'} gone: {w1}"), b1
        else:
            r_ = dict(verdict=v0, stand_at=None if b0 is None else [round(float(b0[0]), 2), round(float(b0[1]), 2)], stand_dist_m=None if b0 is None else round(d0, 2),
                      grasp_height_m=round(zg, 2), clear_first=[], why=w0), b0
        if t in ("side", "edge"):
            r_[0]["why"] += f" (hand comes in from its {t} grasp's side)"
        k = (rank[r_[0]["verdict"]], gv != "yes", type_rank(o, t) if t else 9, c["score"])
        if best is None or k < best[0]:
            best = (k, r_, (t, c, gv, notes))
    res = dict(basis=BASIS, method=f"distance from the grasp point to the nearest place the pelvis may stand (0.22 m from furniture; side / edge grasps only from their own side); reach limits {REACH_MAP and 'MEASURED where the map has the height, else ' or ''}ASSUMED {REACH_YES} m yes / {REACH_MARGINAL} m marginal")
    if best is None:
        o.grasp_used = None
        return dict(res, verdict="no", stand_at=None, stand_dist_m=None, clear_first=[], why="no usable grasp has a standing place (an edge grasp's slide is blocked by things that stay)"), None
    o.grasp_used = best[2] if best[2][0] else None
    r_, b = best[1]
    return dict(res, **r_, grasp_type=best[2][0]), b


def surface_reach_v1(o):
    """A thing on furniture: how near can the pelvis stand (now / with the movable things gone)."""
    xy = o.c[:2]; zg = float(o.plo[2] + min(0.5 * (o.phi[2] - o.plo[2]), 0.12))
    res = dict(basis=BASIS, method=f"distance from the thing to the nearest place the pelvis may stand (0.22 m from furniture); reach {REACH_YES} m yes / {REACH_MARGINAL} m marginal is ASSUMED, not measured")
    b0, d0 = nearest_stand(xy, set()); v0, w0 = reach_verdict(d0, zg)
    b1, d1 = nearest_stand(xy, ALL_MOVED); v1, w1 = reach_verdict(d1, zg)
    rank = {"yes": 0, "marginal": 1, "no": 2}
    if rank[v1] < rank[v0]:
        i, j = cell(b1)
        blk = [n for n, a in loose_clear.items() if a[i, j] <= -0.06 or not state(ALL_MOVED - {n})["stand"][i, j]]
        return dict(res, verdict="after clearing" if v1 == "yes" else "marginal", stand_at=[round(float(b1[0]), 2), round(float(b1[1]), 2)], stand_dist_m=round(d1, 2),
                    grasp_height_m=round(zg, 2), clear_first=blk, why=f"now: {w0}. With {', '.join(blk) or 'the movable things'} gone: {w1}"), b1
    return dict(res, verdict=v0, stand_at=None if b0 is None else [round(float(b0[0]), 2), round(float(b0[1]), 2)], stand_dist_m=None if b0 is None else round(d0, 2),
                grasp_height_m=round(zg, 2), clear_first=[], why=w0), b0


CARRY2_AHEAD = (0.30, 0.33, 0.36, 0.40)                  # m, pelvis to the handlebar for the two-hand take (basket take: 0.42 in the deep squat; standing: ASSUMED)


def carry2_stance(stem, u, ignore, own):
    """Standing place facing the handlebar from the stem side (the deck points away from the robot): the pelvis
    CARRY2_AHEAD m from the stem, opposite the deck, heading within 30 deg of the deck direction."""
    S = state(ignore)
    for a_deg in (0, 15, -15, 30, -30):
        uu = _rot(math.radians(a_deg)) @ u
        for r_ in CARRY2_AHEAD:
            b = stem - r_ * uu
            if np.all(b > LO) and np.all(b < HI) and S["stand"][cell(b)] and float(S["clear"][cell(b)]) > -0.03:
                return b, math.atan2(uu[1], uu[0]), r_
    return None, None, None


def big_reach(o):
    """carry2: the take stance at the handlebar now (or after clearing), and the set-down stance at its place."""
    ph = BIG[o.name]["physics"]; stem = np.array(ph["handlebar"]["stem_scene"]); u = np.array(ph["handlebar"]["deck_dir"], float); u /= np.linalg.norm(u)
    res = dict(basis=BASIS, method="carry2 take stance: standing, facing the handlebar from the stem side, pelvis 0.30-0.40 m from the stem (ASSUMED, the two-hand take is not built)")
    sp = V3_SPOT.get(o.name)
    b, yw, r_ = carry2_stance(stem, u, {o.name}, o.rect)
    clear = []
    if b is None:
        b, yw, r_ = carry2_stance(stem, u, ALL_MOVED, o.rect)
        if b is not None:
            i, j = cell(b); clear = [n for n, a_ in loose_clear.items() if n != o.name and (a_[i, j] <= -0.03 or not state(ALL_MOVED - {n})["stand"][i, j])]
    put = None
    if sp is not None:
        dyaw = math.radians(sp["turn_deg"]); st_t = np.array(sp["stem_target_scene"]); u_t = _rot(dyaw) @ u
        bp, ywp, rp = carry2_stance(st_t, u_t, ALL_MOVED, None)
        put = None if bp is None else dict(stand_scene=[round(float(bp[0]), 2), round(float(bp[1]), 2), round(math.degrees(ywp))], pelvis_to_stem_m=rp)
        o.put_stand = bp
    if b is None:
        return dict(res, verdict="no", why="no standing place facing the handlebar, even with every movable thing gone", stance=None, set_down=put, clear_first=[]), None
    return dict(res, verdict="yes" if not clear else "after clearing", stance=[round(float(b[0]), 2), round(float(b[1]), 2), round(math.degrees(yw))], pelvis_to_stem_m=r_,
                clear_first=clear, set_down=put, why=("standing take place free now" if not clear else "free once " + ", ".join(clear) + " are gone")), b


for o in FREE:
    o.reach, o.stand, o.grasp_used = None, None, None
    if o.status != "mess_to_move":
        continue
    if o.name in BIG and BIG[o.name]["method"] == "carry2":
        o.reach, o.stand = big_reach(o)
        continue
    if o.rest["type"] == "floor":
        o.reach, s = floor_reach(o)
        o.stand = None if s is None else s["xy"]
    else:
        o.reach, o.stand = surface_reach(o)
    if o.name in BIG:                                        # the drag: the floor reach chose the rim grasp; the method stays "drag"
        o.reach["grasp_type"] = "drag (rim: " + str(o.grasp_used[0] if o.grasp_used else None) + ")"
        if o.grasp_used:
            o.grasp["candidate"] = dict(point=o.grasp_used[1]["point"], close=o.grasp_used[1]["close"], approach=o.grasp_used[1]["approach"])
        continue
    # the grasp the reach chose (it may be another usable type than the geometric best)
    if o.grasp_used and o.grasp_used[0] not in (None, "cloth") and o.grasp["verdict"] != "no":
        t, c, gv, notes = o.grasp_used
        if (o.mass or 0) > MASS_MARGINAL:
            gv = "marginal"; notes = notes + [f"{o.mass:.2f} kg: heavy for pad friction alone (measured squeeze 6 N a pad)"]
        o.grasp = dict(o.grasp, verdict=gv, type=t, approach=t, why="; ".join(notes), skill=TYPE_SKILL[t], new_type=t != "top_down", needs=c.get("needs", []),
                       width_cm=round(100 * c["width_m"], 1), axis_deg=round(math.degrees(math.atan2(c["close"][1], c["close"][0]))) % 180,
                       candidate=dict(point=c["point"], close=c["close"], approach=c["approach"], jaw_gap_m=c["jaw_gap_m"], bite_m=c["bite_m"],
                                      **{k: c[k] for k in ("slide_m", "pitch_down_deg", "wall_thickness_m", "overhang_m", "height_above_support_m") if k in c}))

# ---------------------------------------------------------------- destinations and target spots
def aabb(o):
    return (o.plo[:2].copy(), o.phi[:2].copy())


def free_spot(lo, hi, occupied, need, anchor, max_stand=REACH_YES, margin=0.02, step=0.02):
    """A free place for a footprint `need` (x, y size) inside the rectangle lo..hi, clear of `occupied` boxes, nearest
    to where the robot can stand (final floor) and to `anchor`."""
    S = state(ALL_MOVED); best = None
    for x in np.arange(lo[0] + need[0] / 2 + margin, hi[0] - need[0] / 2 - margin + 1e-9, step):
        for y in np.arange(lo[1] + need[1] / 2 + margin, hi[1] - need[1] / 2 - margin + 1e-9, step):
            a, b = np.array([x - need[0] / 2 - margin, y - need[1] / 2 - margin]), np.array([x + need[0] / 2 + margin, y + need[1] / 2 + margin])
            if any(np.all(a < oh) and np.all(b > ol) for ol, oh in occupied):
                continue
            dd = np.where(S["stand"], np.hypot(XS - x, YS - y), np.inf); ds = float(dd.min())
            cost = max(ds, 0.30) + 0.3 * math.hypot(x - anchor[0], y - anchor[1]) + (10.0 if ds > max_stand else 0.0)
            if best is None or cost < best[0]:
                best = (cost, np.array([x, y]), ds)
    return (None, None) if best is None else (best[1], best[2])


def best_spot(lo, hi, occupied, need, anchor, **kw):
    """free_spot for the footprint either way round; returns (centre, stand distance, footprint used)."""
    best = None
    for nd in (tuple(need), tuple(need[::-1])):
        c_, ds = free_spot(lo, hi, occupied, nd, anchor, **kw)
        if c_ is not None and (best is None or ds < best[1] - 0.02):
            best = (c_, ds, nd)
    return best if best else (None, None, tuple(need))


def on_surface(name):
    return [aabb(q) for q in FREE if q.rest["support"] == name and q.status != "mess_to_move"]


DEST = {
    TOY: dict(name="r186i1_basket", kind="low open basket 33 x 27 x 12 cm, 0.3 kg (movable: carried to the rug toys and back)", put="put_down (lower into a low basket)", xy=OBJ["r186i1_basket"].c[:2], z=0.0),
    CORNER: dict(name="floor beside r186i1_basket / r185i1_megabloks_bag (toy corner)", kind="floor spot", put="put_down (set on the floor)", xy=None, z=0.0),
    RUB: dict(name="rubbish_bin", kind="our added open-top bin 32 x 32 x 40 cm, 1.5 kg (movable)", put="drop_in", xy=BIN["xy"], z=0.40),
    HAM: dict(name="r133i1_laundry_basket", kind="open-top hamper 51 x 51 x 65 cm (our replacement of the closed one), not carried", put="drop_in", xy=OBJ["r133i1_laundry_basket"].c[:2], z=0.65),
    SINK: dict(name="r27i1_sink", kind="kitchen sink basin (fixed), rim 0.88-0.91 m", put="drop_in_sink (lower into the basin)", xy=np.array([4.80, 2.00]), z=0.70),
    MAT: dict(name="r119i1_mat", kind="doormat 90 x 60 cm (flat)", put="put_down (set on the mat)", xy=OBJ["r119i1_mat"].c[:2], z=0.01),
    CON: dict(name="r110i1_console", kind="console table top 100 x 38 cm at 0.72 m", put="place_on (set on a table)", xy=OBJ["r110i1_console"].c[:2], z=0.72),
    ISL: dict(name="r35i1_top", kind="kitchen island top 180 x 82 cm at 0.91 m", put="place_on (set on a counter)", xy=OBJ["r35i1_top"].c[:2], z=0.91),
    TRAY: dict(name="r94i1_tray_table", kind="tray table top 40 x 50 cm at 0.78 m", put="place_on (set on a table)", xy=OBJ["r94i1_tray_table"].c[:2], z=0.78),
}
# v3 destinations. The fridge: its compartment is hollow in the collision model (ray-tested with the doors open: rays
# at 0.6-1.5 m go 0.85 m in, to the back wall at y 2.45; no shelf colliders); the floor of the compartment by a ray down
_dd2 = mujoco.MjData(m); _dd2.qpos[:] = m.qpos0
for n_ in ("r34i1_fresh_door", "r34i1_freezer_door"):
    _dd2.qpos[m.jnt_qposadr[m.joint(OBJ[n_].id + "_joint").id]] = 1.6
mujoco.mj_kinematics(m, _dd2)
_gid = np.array([-1], np.int32)
FRIDGE_SHELVES = []                                          # every upward-facing surface in a vertical line through the compartment (x 3.2 / 2.95, y 2.15)
for _x in (3.2, 2.95):
    _z = 1.74
    while _z > 0.05:
        _dist = float(mujoco.mj_ray(m, _dd2, np.array([_x, 2.15, _z]), np.array([0.0, 0.0, -1.0]), None, 1, -1, _gid))
        if _dist < 0:
            break
        _hz = _z - _dist
        FRIDGE_SHELVES.append((round(_x, 2), round(_hz, 3), m.geom(_gid[0]).name))
        _z = _hz - 0.02
FRIDGE_REACHABLE = [s for s in FRIDGE_SHELVES if 0.45 <= s[1] <= 1.05]
FRIDGE_FLOOR_Z = max(FRIDGE_REACHABLE, key=lambda s: s[1])[1] if FRIDGE_REACHABLE else (FRIDGE_SHELVES[-1][1] if FRIDGE_SHELVES else None)
FRIDGE_FLOOR_HIT = [s[1] for s in FRIDGE_SHELVES]
del _dd2


def _spot_xy(n_, default=None):
    return np.asarray(V3_SPOT[n_]["xy"], float) if n_ in V3_SPOT else default


DEST.update({
    PARK: dict(name="vehicle corner (hall wall, beside the toy bike)", kind="floor places, one per scooter, deck across the wall, nose 3-6 cm off the baseboard, handlebar out",
               put="set_down (carry2: walk in nose first, lower both hands until the wheels touch, open both jaws)", xy=_spot_xy("r127i1_scooter", OBJ["r128i1_bike"].c[:2]), z=0.0),
    ENTRY: dict(name="by the entry (floor)", kind="floor places clear of every door's swing", put="put_down (set on the floor)",
                xy=_spot_xy("r107i1_umbrella", FRONT_DOOR_XY), z=0.0),
    UMBW: dict(name=("by the entry (floor)" if (UMB_CHOICE or "").startswith("by the entry") else
                     "against the wall: " + ", ".join(V3_SPOT.get("r106i1_umbrella", {}).get("against", [])[:2]) + f" at ({_spot_xy('r106i1_umbrella', np.zeros(2))[0]:.2f}, {_spot_xy('r106i1_umbrella', np.zeros(2))[1]:.2f}) (floor)"),
               kind="a floor place for the open 1.10 x 0.96 m umbrella, clear of every door's swing, the least walking cost", put="let go of the dragged rim",
               xy=_spot_xy("r106i1_umbrella", FRONT_DOOR_XY), z=0.0),
    BOXW: dict(name="against the wall by the two-tier table (floor)", kind="floor place", put="put_down (set on the floor)", xy=_spot_xy("r175i1_cardboard_box", OBJ["r175i1_cardboard_box"].c[:2]), z=0.0),
    BAGS: dict(name="floor beside the standing bags (by the entry)", kind="floor place", put="put_down (lower the bag hanging from its handles until it stands, open)",
               xy=_spot_xy("r70i1_tote", np.array([5.0, -0.9])), z=0.0),
    TVTOP: dict(name="r159i1_cabinet", kind="TV cabinet top 200 x 46 cm at 0.50 m (TV, books and the hair dryer on it)", put="place_on (set on a low cabinet: half squat)",
                xy=OBJ["r159i1_cabinet"].c[:2], z=0.50),
    FRIDGE: dict(name="r34i1_body", kind=f"fridge compartment (hollow in the collision model; shelf used {FRIDGE_FLOOR_Z} m, all shelves {sorted(set(FRIDGE_FLOOR_HIT))}); doors r34i1_fresh_door / r34i1_freezer_door",
                 put="OPTIONAL fridge round: open the door, place_on the compartment floor, close the door (door skill not built)", xy=np.array([3.2, 2.15]), z=FRIDGE_FLOOR_Z),
})


def dims(o):
    h = o.rect.h if hasattr(o, "rect") else None
    if h is None:
        c, h, _ = NAV.min_rect(o.P[:: len(o.P) // 400 + 1])
    return 2 * float(max(h)), 2 * float(min(h))               # long, short side of its footprint


SPOT = {k_: dict(v_) for k_, v_ in V3_SPOT.items()}       # name -> dict(xy, z, note); v3: the big things' places first
# shoes: pairs side by side on the free part of the mat, long side toward the wall (y)
mat = OBJ["r119i1_mat"]
lamp = OBJ["r109i1_lamp"]; Pl = lamp.P[lamp.P[:, 2] < 0.30]
occ_mat = [(Pl[:, :2].min(0), Pl[:, :2].max(0))] if len(Pl) else [aabb(lamp)]
occ_mat += [aabb(q) for q in FREE if q.rest["type"] == "floor" and q.status != "mess_to_move" and q is not mat and q is not lamp
            and np.all(q.plo[:2] < mat.hi[:2]) and np.all(q.phi[:2] > mat.lo[:2])]
PAIRS = [("r124i2_sandal", "r124i1_sandal"), ("r105i1_shoe", "r105i2_shoe"), ("r125i1_flat", "r125i2_flat"), ("r122i1_croc", "r123i1_slipper")]
for a_, b_ in PAIRS:
    A, B = OBJ[a_], OBJ[b_]
    (la, sa), (lb, sb) = dims(A), dims(B)
    if A.status != "mess_to_move":                           # the sandal already on the mat: its partner goes beside it
        cands = [A.c[:2] + np.array(v) for v in ((0, sb / 2 + sa / 2 + 0.03), (0, -(sb / 2 + sa / 2 + 0.03)), (-(la / 2 + lb / 2 + 0.03), 0), (la / 2 + lb / 2 + 0.03, 0))]
        got = None
        for c_ in cands:
            lo_, hi_ = c_ - np.array([lb, sb]) / 2 - 0.02, c_ + np.array([lb, sb]) / 2 + 0.02
            if np.all(lo_ > mat.lo[:2]) and np.all(hi_ < mat.hi[:2]) and not any(np.all(lo_ < oh) and np.all(hi_ > ol) for ol, oh in occ_mat if not np.allclose(ol, aabb(A)[0])):
                got = c_; break
        if got is None:
            got, _ = free_spot(mat.lo[:2], mat.hi[:2], occ_mat, (lb, sb), A.c[:2], max_stand=0.6)
        if got is not None:
            SPOT[b_] = dict(xy=got, z=0.01, pair_with=a_, note="beside its partner, which is already on the mat")
            occ_mat.append((got - np.array([lb, sb]) / 2, got + np.array([lb, sb]) / 2))
        continue
    need = (sa + sb + 0.03, max(la, lb))
    c_, ds = free_spot(mat.lo[:2], mat.hi[:2], occ_mat, need, mat.c[:2], max_stand=0.6)
    if c_ is None:
        for n_ in (a_, b_):
            SPOT[n_] = dict(xy=None, z=0.01, pair_with=b_ if n_ == a_ else a_, note="NO free place left on the mat for this pair (lamp base and the other pairs fill it): set beside the mat")
        continue
    SPOT[a_] = dict(xy=c_ + np.array([-(sb + 0.03) / 2, 0.0]), z=0.01, pair_with=b_, note="pair side by side, toes to the wall")
    SPOT[b_] = dict(xy=c_ + np.array([(sa + 0.03) / 2, 0.0]), z=0.01, pair_with=a_, note="pair side by side, toes to the wall")
    occ_mat.append((c_ - np.array(need) / 2, c_ + np.array(need) / 2))
# v3: a pair with no room left on the mat stands on the floor right beside the mat (shoes in a row, not on the walkway)
mat_open = [(a_, b_) for a_, b_ in PAIRS if SPOT.get(a_, {}).get("xy", 0) is None and OBJ[a_].status == "mess_to_move"]
for a_, b_ in mat_open:
    for n_ in (a_, b_):
        o_ = OBJ[n_]; h_ = o_.rect.h; best_ = None
        for yw_ in (0.0, math.pi / 2):
            for x in np.arange(mat.lo[0] - 0.45, mat.hi[0] + 0.45, 0.04):
                for y in np.arange(mat.lo[1] - 0.45, mat.hi[1] + 0.45, 0.04):
                    ok_, _ = spot_clear((x, y), h_, yw_, margin=0.02, extra_avoid=[(np.asarray(s_["xy"]) - 0.08, np.asarray(s_["xy"]) + 0.08, k_) for k_, s_ in SPOT.items()
                                                                                    if s_.get("xy") is not None and k_ != n_ and OBJ.get(k_) is not None and OBJ[k_].cls == "shoe"])
                    if not ok_:
                        continue
                    dm_ = float(np.linalg.norm(np.maximum(np.maximum(mat.lo[:2] - (x, y), 0), (x, y) - mat.hi[:2])))
                    partner_ = SPOT.get(b_ if n_ == a_ else a_, {}).get("xy")
                    cst_ = dm_ + (0.0 if partner_ is None else 0.5 * abs(float(np.linalg.norm(np.asarray(partner_) - (x, y))) - 0.16))
                    if best_ is None or cst_ < best_[0]:
                        best_ = (cst_, np.array([x, y]), yw_)
        if best_ is not None:
            SPOT[n_] = dict(xy=best_[1], z=0.01, pair_with=b_ if n_ == a_ else a_, note=f"no room left on the mat (lamp base + 3 pairs): on the floor beside the mat, {best_[0]:.2f} m off it, with its partner (v3)")
# things set on furniture: a free place near the edge the robot can stand at
for dk, sup in ((CON, "r110i1_console"), (ISL, "r35i1_top"), (TRAY, "r94i1_tray_table"), (TVTOP, "r159i1_cabinet")):
    occ = on_surface(sup); s_ = OBJ[sup]
    for o in [q for q in MESS if q.dest == dk]:
        l_, w_ = dims(o)
        c_, ds, nd = best_spot(s_.lo[:2], s_.hi[:2], occ, (l_, w_), s_.c[:2], max_stand=REACH_MARGINAL)
        if c_ is None:
            SPOT[o.name] = dict(xy=None, z=DEST[dk]["z"], note=f"NO free place of {100 * l_:.0f} x {100 * w_:.0f} cm left on {sup}: something there has to be moved together first")
        else:
            SPOT[o.name] = dict(xy=c_, z=DEST[dk]["z"], note=f"free place on {sup}, {ds:.2f} m from where the pelvis can stand")
            occ.append((c_ - np.array(nd) / 2, c_ + np.array(nd) / 2))
# the two big toys: on the floor of the toy corner
occ = [(r.c - np.abs(r.R) @ r.h, r.c + np.abs(r.R) @ r.h) for r in base_rects if np.linalg.norm(r.c - DEST[TOY]["xy"]) < 2.5] + [aabb(OBJ["r186i1_basket"])]
for n_ in ("r188i1_dollhouse", "r130i1_light_saber", "r154i1_stick"):
    l_, w_ = dims(OBJ[n_]); a0 = DEST[TOY]["xy"]
    c_, ds = free_spot(a0 - np.array([0.9, 1.0]), a0 + np.array([1.2, 1.0]), occ, (w_, l_), a0, max_stand=0.5)
    SPOT[n_] = dict(xy=c_, z=0.0, note="free floor beside the toy basket" if c_ is not None else "NO free floor found within 1 m of the toy basket")
    if c_ is not None:
        occ.append((c_ - np.array([w_, l_]) / 2, c_ + np.array([w_, l_]) / 2))


def dest_spot(o):
    if o.name in SPOT:
        return SPOT[o.name]
    return dict(xy=DEST[o.dest]["xy"], z=DEST[o.dest]["z"], note="anywhere inside")


# where the robot stands to serve each destination (final floor; the container itself is not in the way of its own stance)
def dest_stand(xy, ignore=ALL_MOVED):
    return nearest_stand(np.asarray(xy, float), ignore)


DEST_INFO = {}
for k, D in DEST.items():
    if D["xy"] is None:
        continue
    b, ds = dest_stand(D["xy"])
    b_now, ds_now = nearest_stand(D["xy"], set())
    v, w = reach_verdict(ds, min(D["z"] + 0.10, 1.0))
    DEST_INFO[k] = dict(name=D["name"], kind=D["kind"], put_skill=D["put"], centre=[round(float(D["xy"][0]), 2), round(float(D["xy"][1]), 2)], rim_or_top_m=D["z"],
                        stand_at=None if b is None else [round(float(b[0]), 2), round(float(b[1]), 2)], stand_dist_m=round(ds, 2), stand_dist_now_m=round(ds_now, 2),
                        reach=v, reach_why=w + (f" (now, before anything is cleared: {ds_now:.2f} m)" if abs(ds_now - ds) > 0.03 else ""), basis=BASIS)
    D["stand"] = b if b is not None else np.asarray(D["xy"], float)
DEST[CORNER]["stand"] = DEST[TOY]["stand"]

# ---------------------------------------------------------------- the sink (v2): no collider in the pack; stance with the dishwasher closed / open
# The pack's sink r27i1 is drawn only (0 collision pieces) and the countertop's collider has a hole there: a dish let go
# over the basin falls through into the corner cabinet (its bottom panel at 0.12 m; ray cast through the collision geoms).
# Basin from the sink's visual mesh: a box turned 45 deg, centre (4.805, 2.005), inside 0.424 x 0.524 m, floor 0.668-0.68 m,
# straight walls to the rim at 0.87-0.88 m. SINK_COLLIDER below is a fixed 'extras' entry for OUR merged model (5 boxes).
SINK_R = dict(c=np.array([4.805, 2.005]), h=np.array([0.212, 0.262]), yaw=math.radians(45.0), z_floor=0.68, z_rim=0.88)
SINK_COLLIDER = dict(name="sink_basin_collider", kind="fixed", pose=[4.805, 2.005, 45.0], z=0.668, mass=1.0, cls="sink", role="sink", accepts=["dish"], rgba=[0, 0, 0, 0],
                     friction=0.6, boxes=[dict(c=[0.0, 0.0, 0.006], s=[0.424, 0.524, 0.012]),
                                          dict(c=[0.217, 0.0, 0.106], s=[0.01, 0.544, 0.212]), dict(c=[-0.217, 0.0, 0.106], s=[0.01, 0.544, 0.212]),
                                          dict(c=[0.0, 0.267, 0.106], s=[0.444, 0.01, 0.212]), dict(c=[0.0, -0.267, 0.106], s=[0.444, 0.01, 0.212])],
                     note="the pack's sink has no collider; scene frame pose; invisible (hide its prims after import if the importer draws them); by geometry, not verified")


def basin_points(margin=0.06, step=0.02):
    Rm = R2(SINK_R["yaw"]); h = SINK_R["h"] - margin
    g = [(x, y) for x in np.arange(-h[0], h[0] + 1e-9, step) for y in np.arange(-h[1], h[1] + 1e-9, step)]
    return np.array([SINK_R["c"] + Rm @ np.array(p) for p in g])


def stand_from_clear(clear):
    lab, _ = ndimage.label(clear > 0, structure=S3)
    i, j = cell(START)
    if lab[i, j] == 0:
        dd = np.where(lab > 0, np.hypot(XS - START[0], YS - START[1]), np.inf); i, j = np.unravel_index(np.argmin(dd), dd.shape)
    return ndimage.binary_dilation(lab == lab[i, j], structure=S3, iterations=5) & (clear > -0.06)


def nearest_pair(stand, targets):
    """(stand cell, target point, distance) of the closest standing cell to any of the target points."""
    cells = np.argwhere(stand)
    if not len(cells):
        return None, None, float("inf")
    P_ = np.c_[XS[stand], YS[stand]]
    D_ = np.linalg.norm(P_[:, None, :] - np.asarray(targets)[None, :, :2], axis=2) if len(P_) * len(targets) < 4e6 else None
    if D_ is None:
        from scipy.spatial import cKDTree
        dd, ii = cKDTree(np.asarray(targets)[:, :2]).query(P_); k = int(np.argmin(dd)); return P_[k], np.asarray(targets)[ii[k]], float(dd[k])
    k = np.unravel_index(np.argmin(D_), D_.shape)
    return P_[k[0]], np.asarray(targets)[k[1]], float(D_[k])


BASIN = basin_points()
scrap_rects = []
for n_ in WALK_OVER_THIN:
    q_ = OBJ[n_]; c_, h_, y_ = NAV.min_rect(q_.P[:: len(q_.P) // 400 + 1]); r_ = NAV.Rect(c_, h_, y_, low=True, name=n_); r_.top = float(q_.phi[2]); scrap_rects.append(r_)
import copy
SINK_VARIANTS = {}
for key_, rects_ in (("dishwasher closed, feet may step on the paper scraps (the plan)", base_closed + [r for r in base_rects if not r.fixed]),
                     ("dishwasher closed, feet kept off the paper scraps", base_closed + [r for r in base_rects if not r.fixed] + scrap_rects),
                     ("dishwasher closed, furniture as axis-aligned boxes (as the room builder makes them)", base_closed_aabb + [r for r in base_rects if not r.fixed]),
                     ("dishwasher closed, fixed pieces under 15 cm high (the corner cabinet's 12 cm bottom panel, sticking out 25 cm in front of its diagonal face) "
                      "kept only 16 cm from the feet instead of 28 cm from the pelvis", [copy.copy(r) for r in base_closed] + [r for r in base_rects if not r.fixed]),
                     ("dishwasher open (as the pack is), feet may step on the scraps", base_open),
                     ("dishwasher open, feet kept off the scraps (v1's condition)", base_open + scrap_rects)):
    if key_.startswith("dishwasher closed, fixed pieces under 15 cm"):
        for r in rects_:
            if getattr(r, "fixed", False) and r.top < 0.15:
                r.low = True
    G_ = NAV.Grid(LO, HI, rects_, res=RES, r_body=R_BODY, r_foot=R_FOOT)
    b_, p_, d_ = nearest_pair(stand_from_clear(G_.clear), BASIN)
    v_, w_ = reach_verdict(d_, 0.95)
    SINK_VARIANTS[key_] = dict(stand_at=None if b_ is None else [round(float(b_[0]), 2), round(float(b_[1]), 2)], drop_point=None if p_ is None else [round(float(p_[0]), 2), round(float(p_[1]), 2)],
                               dist_m=round(d_, 2), reach=v_, why=w_)
S_fin = state(ALL_MOVED)
if "--debug-sink" in sys.argv:
    for pt in ((4.35, 1.55), (4.30, 1.50), (4.40, 1.45), (4.45, 1.35)):
        i_, j_ = cell(pt)
        near_ = sorted((float(r.dist(np.array([pt]))[0]) - (R_FOOT if r.low else R_BODY), r.name, round(math.degrees(r.yaw))) for r in base_rects)[:4]
        print("DEBUG", pt, "clear", round(float(S_fin["clear"][i_, j_]), 3), "main", bool(S_fin["main"][i_, j_]), "stand", bool(S_fin["stand"][i_, j_]), near_)
    for r in base_rects:
        if r.name in ("r21i1_corner", "r26i1_countertop"):
            print("DEBUG rect", r.name, np.round(r.c, 3), np.round(r.h, 3), round(math.degrees(r.yaw)), type(r).__name__, round(r.top, 2))
b_s, p_s, d_s = nearest_pair(S_fin["stand"], BASIN)
v_s, w_s = reach_verdict(d_s, 0.95)
DEST[SINK]["xy"] = p_s if p_s is not None else DEST[SINK]["xy"]; DEST[SINK]["stand"] = b_s if b_s is not None else DEST[SINK]["stand"]
DEST_INFO[SINK].update(stand_at=None if b_s is None else [round(float(b_s[0]), 2), round(float(b_s[1]), 2)], stand_dist_m=round(d_s, 2), reach=v_s,
                       reach_why=w_s + " (to the nearest point 6 cm inside the basin; dishwasher " + ("closed by the optional step" if DW_CLOSE else "open") + ")",
                       centre=[round(float(SINK_R["c"][0]), 2), round(float(SINK_R["c"][1]), 2)], drop_point=[round(float(DEST[SINK]["xy"][0]), 2), round(float(DEST[SINK]["xy"][1]), 2)],
                       variants=SINK_VARIANTS, collider="NONE in the pack: use SINK_COLLIDER (room_patch.json extras)")
# the optional step itself: where the robot stands to push the racks in and lift the door (dishwasher open, today's floor)
S_open_now = stand_from_clear(np.minimum(G0_OPEN.clear, np.min([a for a in loose_clear.values()], axis=0)))
DW_TARGETS = {"top rack front (pulled out), 0.46-0.63 m": (np.array([[3.76, 1.52], [4.01, 1.52], [4.26, 1.52]]), 0.55),
              "bottom rack front (pulled out), 0.15-0.31 m": (np.array([[3.76, 1.57], [4.01, 1.57], [4.26, 1.57]]), 0.25),
              "door's free edge (open, lying), 0.06-0.13 m": (np.array([[3.75, 1.17], [4.01, 1.17], [4.27, 1.17]]), 0.10)}
DW_INFO = {}
for k_, (tg_, z_) in DW_TARGETS.items():
    b_, p_, d_ = nearest_pair(S_open_now, tg_)
    v_, w_ = reach_verdict(d_, z_)
    DW_INFO[k_] = dict(stand_at=None if b_ is None else [round(float(b_[0]), 2), round(float(b_[1]), 2)], hand_at=None if p_ is None else [round(float(p_[0]), 2), round(float(p_[1]), 2)],
                       dist_m=round(d_, 2), reach=v_, why=w_)
DW_STAND = np.array(DW_INFO["top rack front (pulled out), 0.46-0.63 m"]["stand_at"] or [4.0, 0.9])

# ---------------------------------------------------------------- target spots inside the containers (v2: one per object)
def slots_in_rect(c, h, yaw, step, margin):
    Rm = R2(yaw); hh = np.maximum(h - margin, 0.0)
    xs = np.arange(-hh[0], hh[0] + 1e-9, step) if hh[0] > 0 else [0.0]
    ys = np.arange(-hh[1], hh[1] + 1e-9, step) if hh[1] > 0 else [0.0]
    return [c + Rm @ np.array([x, y]) for x in xs for y in ys]


_sink_slots = sorted(slots_in_rect(SINK_R["c"], SINK_R["h"], SINK_R["yaw"], 0.11, 0.07), key=lambda p: float(np.linalg.norm(p - DEST[SINK]["stand"])))
for i_, o in enumerate(sorted([q for q in MESS if q.dest == SINK], key=lambda q: q.name)):
    if o.name not in SPOT:
        p_ = _sink_slots[i_ % len(_sink_slots)]; lay = i_ // len(_sink_slots)
        SPOT[o.name] = dict(xy=p_, z=round(SINK_R["z_floor"] + 0.02 + 0.06 * lay, 3), note=f"slot {i_ + 1} on the basin floor (nearest the stance first){'; on top of another dish' if lay else ''}; release about 0.95 m up")
bk = OBJ["r186i1_basket"]; pl_ = OBJ["r187i1_plush"]
_bk_slots = sorted(slots_in_rect((bk.plo[:2] + bk.phi[:2]) / 2, (bk.phi[:2] - bk.plo[:2]) / 2, 0.0, 0.10, 0.06),
                   key=lambda p: bool(np.all(p > pl_.plo[:2] - 0.03) and np.all(p < pl_.phi[:2] + 0.03)))      # beside the plush first, then on it
for i_, o in enumerate(sorted([q for q in MESS if q.dest == TOY], key=lambda q: q.name)):
    if o.name not in SPOT and _bk_slots:
        lay = i_ // len(_bk_slots); p_ = _bk_slots[i_ % len(_bk_slots)]
        on_plush = bool(np.all(p_ > pl_.plo[:2] - 0.03) and np.all(p_ < pl_.phi[:2] + 0.03))
        z0 = float(pl_.phi[2]) + 0.02 if on_plush else float(bk.plo[2]) + 0.03
        SPOT[o.name] = dict(xy=p_, z=round(z0 + 0.05 * lay, 3),
                            note=f"slot {i_ % len(_bk_slots) + 1} of {len(_bk_slots)} in the toy basket" + (" (on top of the plush already in it)" if on_plush else "") + f", layer {lay + 1}"
                                 + (" (heaped above the 12 cm rim: overflow to the megabloks bag beside it)" if z0 + 0.05 * lay > float(bk.phi[2]) else ""))
for o in MESS:
    if o.name in SPOT:
        continue
    if o.dest == RUB:
        SPOT[o.name] = dict(xy=BIN["xy"].copy(), z=0.50, note="let go over the middle of the bin's opening, 10 cm above its 0.40 m rim")
    elif o.dest == HAM:
        hm = OBJ["r133i1_laundry_basket"]
        SPOT[o.name] = dict(xy=(hm.plo[:2] + hm.phi[:2]) / 2, z=0.75, note="let go over the middle of the open-top hamper, 10 cm above its 0.65 m rim (cloth agent's drop_in_cloth)")

# ---------------------------------------------------------------- which mess is planned, which is skipped
for o in MESS:
    o.planned, o.skip = True, None
    if o.grasp["verdict"] == "no":
        o.planned, o.skip = False, "not graspable: " + o.grasp["why"]
    elif o.reach["verdict"] == "no":
        o.planned, o.skip = False, "not reachable: " + o.reach["why"]
    elif o.name in SPOT and SPOT[o.name]["xy"] is None:
        o.planned, o.skip = False, SPOT[o.name]["note"]
    elif DEST_INFO.get(o.dest, {}).get("reach") == "no" and o.dest not in (PARK, ENTRY, UMBW):
        o.planned, o.skip = False, f"its destination {DEST[o.dest]['name']} cannot be reached: {DEST_INFO[o.dest]['reach_why']}"
    if o.dest == FRIDGE:
        o.planned, o.skip = False, ("OPTIONAL fridge round, not in the route: the fridge doors are frozen in our rooms and no door skill exists (the surface agent is building one for "
                                    "the dishwasher); with it: open r34i1_fresh_door, set the jug on the compartment floor, close the door. " + (o.skip or ""))
PLAN = [o for o in MESS if o.planned]


def skills_of(o):
    floor = o.rest["type"] == "floor"; D = DEST[o.dest]
    if o.name in BIG:
        meth = BIG[o.name]["method"]
        return dict(pick=meth, pick_status="NOT BUILT: " + ("two-hand take of the handlebar, stand, walk, set down (the toy-basket carry, basket_skills.take_basket / set_basket_down, is the pattern)"
                                                            if meth == "carry2" else "floor side grasp of the rim in the deep squat, stand up holding, walk with the far rim sliding, let go"),
                    grasp_type=meth, grasp_skill=o.grasp.get("skill"), grasp_basis=BASIS + ": NEW method, the live agents confirm or reject it",
                    surface_height_band="floor", put=D["put"], put_status="NOT BUILT (part of the same new step)", needs_two_hands=meth == "carry2",
                    needs_door_or_drawer_open=False, container_carry=False, needs_collider=None, put_needs_collider=None, physics=BIG[o.name]["physics"])
    cloth = o.name in CLOTH
    two = (o.name in CLOTH_BIG) or (o.mass or 0) > 1.0
    pick = "cloth_pick" if cloth else ("floor_pick" if floor else "surface_pick")
    status = {"floor_pick": "exists: proven on one toy piece (run 1118_193303); top-down only",
              "cloth_pick": "grasp_cloth written by the cloth agent from its live knit-hat runs (E:/urc_cloth, commit cf4eabf); the other six garments not tried yet",
              "surface_pick": "NOT BUILT (no pick from furniture exists)"}[pick]
    put_status = {TOY: "exists: proven once (toy piece into the toy basket)", CORNER: "put_down on the floor: written, a flat destination is not run yet",
                  MAT: "put_down on a flat mat: written, not run yet", RUB: "drop_in: ran in the practice room only, not in the apartment",
                  HAM: "drop_in_cloth into the open-top hamper: written by the cloth agent from its live knit-hat runs (commit cf4eabf; not checked by the planner)" if o.name in CLOTH else "drop_in: ran in the practice room only; the hamper rim is 0.65 m",
                  SINK: "NOT BUILT (place into the sink); the sink needs a collider first (none in the pack)",
                  CON: "NOT BUILT (place_on a table)", ISL: "NOT BUILT (place_on a counter)", TRAY: "NOT BUILT (place_on a table)",
                  PARK: "NOT BUILT (carry2 set-down)", ENTRY: "put_down on a floor spot: written, a flat destination not run yet", BOXW: "put_down on a floor spot: written, not run yet",
                  BAGS: "put_down on a floor spot: written, not run yet (a bag hanging from its handles: lower until it stands)", TVTOP: "place_into / place_on a low cabinet: the surface agent's place_into written, not run (half squat)",
                  FRIDGE: "NOT BUILT (door skill + place inside)", UMBW: "NOT BUILT (let go of the dragged rim at the spot)"}[o.dest]
    if cloth and o.name in CLOTH_ON_FURNITURE:
        status = f"NOT BUILT: a cloth pick from furniture ({CLOTH_ON_FURNITURE[o.name]}); grasp_cloth exists for garments on the floor only; the garment must also be made cloth (PROPOSED)"
    gt = o.grasp.get("type")
    return dict(pick=pick, pick_status=status, grasp_type=gt, grasp_skill=TYPE_SKILL.get(gt, "-") if gt else "-",
                grasp_basis="by geometry, not verified" + ("" if gt in ("top_down", "cloth") else ": NEW grasp type, the live agents confirm or reject it"),
                surface_height_band=band(o.rest["surface_height_m"]) if not floor else "floor", put=D["put"], put_status=put_status,
                needs_two_hands=bool(two), needs_door_or_drawer_open=bool(o.dest == SINK and DW_CLOSE), container_carry=False,
                needs_collider=("hollow collider (hollow_colliders.json)" if gt == "rim_pinch" else None),
                put_needs_collider=("sink basin collider (room_patch.json extras: the pack's sink has none)" if o.dest == SINK else None))


# ---------------------------------------------------------------- walking distances on the final floor
SF = state(ALL_MOVED)
idx = -np.ones((NX, NY), int); cells_main = np.argwhere(SF["main"]); idx[SF["main"]] = np.arange(len(cells_main))
rows, cols, wts = [], [], []
for dx, dy, w in ((1, 0, 1.0), (0, 1, 1.0), (1, 1, 1.4142), (1, -1, 1.4142)):
    a = idx[max(0, -dx):NX - max(0, dx), max(0, -dy):NY - max(0, dy)]
    b = idx[max(0, dx):NX - max(0, -dx), max(0, dy):NY - max(0, -dy)]
    ok = (a >= 0) & (b >= 0)
    rows.append(a[ok]); cols.append(b[ok]); wts.append(np.full(int(ok.sum()), w * RES))
GR = coo_matrix((np.concatenate(wts), (np.concatenate(rows), np.concatenate(cols))), shape=(len(cells_main), len(cells_main))).tocsr()
_node = {}


def node(p):
    """Nearest walkable cell (index) of a point, and the straight rest."""
    key = (round(float(p[0]), 2), round(float(p[1]), 2))
    if key not in _node:
        dd = np.hypot(cells_main[:, 0] * RES + LO[0] - p[0], cells_main[:, 1] * RES + LO[1] - p[1])
        k = int(np.argmin(dd)); _node[key] = (k, float(dd[k]))
    return _node[key]


POINTS = {"start": START}
for o in PLAN:
    POINTS[o.name] = o.stand if o.stand is not None else o.c[:2]
for k, D in DEST.items():
    POINTS["dest:" + k] = D["stand"]
RUG_TOYS = ["r193i1_toy_piece", "r193i2_toy_piece", "r193i3_toy_piece", "r193i4_toy_piece", "r192i1_ball", "r191i1_toy_vehicle", "r190i1_stocking", "r188i1_dollhouse"]
LIVING_RUBBISH = ["r195i1_paper", "r195i2_paper", "r196i1_plastic_bag", "r157i1_paper", "r157i2_paper", "r158i1_tissue", "r149i1_pouch"]


def open_floor_near(xy, room=0.12):
    """Nearest floor cell with `room` to spare on top of the body clearance (a place to set a container down), today's floor."""
    S = state(set())
    dd = np.where(S["main"] & (S["clear"] > room), np.hypot(XS - xy[0], YS - xy[1]), np.inf)
    i, j = np.unravel_index(np.argmin(dd), dd.shape)
    return np.array([XS[i, j], YS[i, j]])


BASKET_AT_RUG = open_floor_near(np.mean([OBJ[n].c[:2] for n in RUG_TOYS if n != "r188i1_dollhouse"], axis=0))
BIN_AT_LIVING = open_floor_near(np.mean([OBJ[n].c[:2] for n in LIVING_RUBBISH], axis=0))
POINTS["spot:basket_at_rug"] = dest_stand(BASKET_AT_RUG)[0]
POINTS["spot:bin_at_living"] = dest_stand(BIN_AT_LIVING)[0]
POINTS["dw:stand"] = DW_STAND
# v3: where the robot ends a big thing's move (carry2 set-down stance / drag release), and the close-door stances
for o in PLAN:
    if o.name in BIG:
        sp_ = SPOT.get(o.name); ps_ = getattr(o, "put_stand", None)
        if ps_ is None and sp_ is not None and sp_["xy"] is not None:
            ps_ = dest_stand(sp_["xy"])[0]
        POINTS["park:" + o.name] = np.asarray(ps_ if ps_ is not None else (sp_["xy"] if sp_ else o.c[:2]), float)
DOOR_STEPS = {}
for n_ in OPEN_DOORS:
    if n_.startswith(("r32i", "r33i")):                       # the dishwasher: v2's close_dishwasher step (racks in, door up)
        continue
    D_ = DOORS[n_]; lo_, hi_ = np.array(D_["box_pack_scene"][0]), np.array(D_["box_pack_scene"][1]); hinge_ = np.array(D_["hinge_or_axis_scene"][:2])
    corners_ = [np.array([x, y]) for x in (lo_[0], hi_[0]) for y in (lo_[1], hi_[1])]
    free_ = max(corners_, key=lambda p: float(np.linalg.norm(p - hinge_))); L_ = float(np.linalg.norm(free_ - hinge_)); ld_ = (free_ - hinge_) / L_
    cc_ = (np.array(D_["box_closed_scene"][0][:2]) + np.array(D_["box_closed_scene"][1][:2])) / 2
    n1_ = np.array([-ld_[1], ld_[0]]); n1_ = n1_ if float(n1_ @ (cc_ - hinge_)) > 0 else -n1_
    push_ = hinge_ + ld_ * 0.85 * L_ - n1_ * 0.03                 # on the open leaf's face, 85 % out from the hinge
    zp_ = round(float((lo_[2] + hi_[2]) / 2), 2)
    b_now, d_now = nearest_stand_dir(push_, set(), n1_, max_angle=50.0)
    b_fin, d_fin = nearest_stand_dir(push_, ALL_MOVED, n1_, max_angle=50.0)
    v_, w_ = reach_verdict(d_fin, zp_)
    DOOR_STEPS[n_] = dict(push_point_scene=[round(float(push_[0]), 2), round(float(push_[1]), 2), zp_], push_dir=[round(float(v), 2) for v in n1_],
                          leaf_length_m=round(L_, 2), arc_m=round(L_ * abs(D_["q_closed"]), 2), hinge_scene=[round(float(v), 2) for v in hinge_],
                          stand_now_scene=None if b_now is None else [round(float(b_now[0]), 2), round(float(b_now[1]), 2)], stand_dist_now_m=round(d_now, 2),
                          stand_scene=None if b_fin is None else [round(float(b_fin[0]), 2), round(float(b_fin[1]), 2)], stand_dist_m=round(d_fin, 2), reach=v_, reach_why=w_,
                          force_note=f"{D_['mass_kg']} kg leaf, hinge damping {D_['damping']} N m s: a few newtons; the stroke follows an arc of {L_ * abs(D_['q_closed']):.2f} m, "
                                     "longer than one arm stroke: push the free end about 0.25 m, step, push again (or let it swing on: damping is low)", basis=BASIS)
    POINTS["door:" + n_] = b_fin if b_fin is not None else push_ - n1_ * 0.4
KEYS = list(POINTS)
SRC_NODES = [node(POINTS[k])[0] for k in KEYS]
DM = dijkstra(GR, directed=False, indices=SRC_NODES)
KI = {k: i for i, k in enumerate(KEYS)}


def walk(a, b):
    """Planned walking distance between two named points (final floor)."""
    if a == b:
        return 0.0
    ka, ra = node(POINTS[a]); kb, rb = node(POINTS[b])
    dd = float(DM[KI[a], kb])
    return (dd if np.isfinite(dd) else float(np.linalg.norm(POINTS[a] - POINTS[b])) * 1.5) + ra + rb


# ---------------------------------------------------------------- the route: blocks in a fixed zone order, trips inside a block chosen greedily
def available(o, removed):
    """Can it be picked now, given what has been taken away already?"""
    need = set(o.reach.get("clear_first") or [])
    if need <= removed:
        return True
    if o.rest["type"] == "floor":                         # another set of neighbours may have freed it
        st, _ = squat_stances(pick_points(o) or [(o.rect.c, None)], o.rect, set(removed) | {o.name})
        return bool(st)
    return False


def pick_time(o, model):
    if o.name in CLOTH:
        return T["cloth_pick_two_hands"] if o.name in CLOTH_BIG else T["cloth_pick"]
    if o.rest["type"] != "floor":
        return T["surface_pick"]
    return T["floor_pick_B2"] if model == "b2" else T["floor_pick"]


def put_time(o, model):
    k = o.dest
    if k in (TOY, CORNER, MAT, ENTRY, BOXW, BAGS):
        return T["put_down_B2"] if model == "b2" else T["put_down"]
    return {RUB: T["drop_in"], HAM: T["drop_in"], SINK: T["sink_drop"]}.get(k, T["place_on"])


def is_single(o):
    return o.name in CLOTH_BIG or (o.mass or 0) > 1.0      # two hands: nothing else in that trip


class Sim:
    def __init__(self):
        self.pos = "start"; self.removed = set(); self.steps = []; self.trips = []; self.deferred = []
        self.m_empty = 0.0; self.m_carry = 0.0; self.t = dict(stated=0.0, b2=0.0, target_lo=0.0, target_hi=0.0, target_model=0.0)

    def leg(self, to, carry):
        L = walk(self.pos, to); self.pos = to
        if carry:
            self.m_carry += L
        else:
            self.m_empty += L
        return L

    def add_time(self, e, c, fixed_stated, fixed_b2, n_items=0, containers=0):
        self.t["stated"] += e / V["stated"]["empty"] + c / V["stated"]["carry"] + fixed_stated
        self.t["b2"] += e / V["b2"]["empty"] + c / V["b2"]["carry"] + fixed_b2
        self.t["target_lo"] += n_items * TARGET_ITEM[0] + containers * (TARGET["container_pick"] + TARGET["container_set"]) + (c / TARGET["carry"] if containers else 0.0)
        self.t["target_hi"] += n_items * TARGET_ITEM[1] + containers * (TARGET["container_pick"] + TARGET["container_set"]) + (c / TARGET["carry"] if containers else 0.0)

    def close_dw(self):
        e = self.leg("dw:stand", False); fx = T["close_dishwasher"]
        self.add_time(e, 0.0, fx, fx); self.t["target_lo"] += fx; self.t["target_hi"] += fx
        self.steps.append(dict(step=["close_dishwasher", {"racks": ["r33i1_rack", "r33i2_rack"], "door": "r32i1_door", "stand_scene": [round(float(v), 2) for v in DW_STAND],
                                                          "stand_world": [round(float(v), 2) for v in (DW_STAND - START)], "optional": True}],
                               what="OPTIONAL: push both dishwasher racks in, lift the door shut (frees the floor in front of the sink)", runs_today=False,
                               needs="NEW: door / drawer skill (not built); the room file must leave these 3 joints free (doors are frozen today)",
                               walk_empty_m=round(e, 2), walk_carry_m=0.0, est_s=dict(stated=round(e / V["stated"]["empty"] + fx), b2=round(e / V["b2"]["empty"] + fx))))

    def big(self, o, label):
        """v3: one big thing to its place by carry2 or drag (NEW step types)."""
        meth = BIG[o.name]["method"]; sp = SPOT[o.name]
        e = self.leg(o.name, False); c = self.leg("park:" + o.name, True)
        fx = (T_BIG["carry2_take"] + T_BIG["carry2_set"]) if meth == "carry2" else (T_BIG["drag_take"] + T_BIG["drag_release"])
        self.add_time(e, c, fx, fx, n_items=1)
        ph = BIG[o.name]["physics"]
        opt = {"to_scene": [round(float(sp["xy"][0]), 3), round(float(sp["xy"][1]), 3), sp["yaw_deg"]],
               "to_world": [round(float(sp["xy"][0] - START[0]), 3), round(float(sp["xy"][1] - START[1]), 3), sp["yaw_deg"]], "turn_deg": sp.get("turn_deg"),
               "hold": True}
        if meth == "carry2":
            opt.update(grip="both hands on the handlebar ends, side grasp round the 2.7 cm bar", handlebar_z=ph["handlebar"]["z_m"], lift_m=0.03,
                       take_stance_scene=o.reach.get("stance"), set_down=o.reach.get("set_down"), stem_target_scene=sp.get("stem_target_scene"), nose_to="wall")
        else:
            opt.update(grip="one hand on the rim at floor level (deep squat, hand pitched down)", grip_point_scene=o.grasp.get("candidate", {}).get("point"),
                       take_stance_scene=o.reach.get("stance"), hand_height_while_dragging_m=ph["drag_by_edge"]["hand_z_m"])
        ts = e / V["stated"]["empty"] + c / V["stated"]["carry"] + fx; tb = e / V["b2"]["empty"] + c / V["b2"]["carry"] + fx
        o.est = dict(today_stated_speeds_s=round(ts), today_run_B2_rates_s=round(tb), target_s=list(TARGET_ITEM), trip_items=[o.name], trip_walk_empty_m=round(e, 2),
                     trip_walk_carry_m=round(c, 2), order_in_route=len(self.trips) + 1)
        self.steps.append(dict(step=[meth, o.name, opt], what=label, runs_today=False,
                               needs=("NEW step type carry2 (not built): two-hand take of the handlebar, stand, walk at the carrying speed, set down nose to the wall"
                                      if meth == "carry2" else "NEW step type drag (not built): rim grasp at floor level, stand up holding, walk, let go at the spot"),
                               grasp_types={meth: 1}, destination=DEST[o.dest]["name"], n_items=1, walk_empty_m=round(e, 2), walk_carry_m=round(c, 2),
                               est_s=dict(stated=round(ts), b2=round(tb))))
        self.removed.add(o.name); self.trips.append([o.name])

    def close_door(self, n_, label):
        """v3: close a door the pack leaves open (NEW step type)."""
        e = self.leg("door:" + n_, False); fx = T_BIG["close_door"]
        self.add_time(e, 0.0, fx, fx); self.t["target_lo"] += fx; self.t["target_hi"] += fx
        ds = DOOR_STEPS[n_]; D_ = DOORS[n_]
        self.steps.append(dict(step=["close_door", n_, {"joint": D_["joint"], "q_closed": D_["q_closed"], "push_point_scene": ds["push_point_scene"],
                                                        "push_point_world": [round(ds["push_point_scene"][0] - START[0], 3), round(ds["push_point_scene"][1] - START[1], 3), ds["push_point_scene"][2]],
                                                        "push_dir": ds["push_dir"], "stand_scene": ds["stand_scene"], "optional": False}],
                               what=label, runs_today=False, needs="NEW step type close_door (not built; the surface agent's door work for the dishwasher is the nearest); the room file must leave this joint free (frozen today)",
                               walk_empty_m=round(e, 2), walk_carry_m=0.0, est_s=dict(stated=round(e / V["stated"]["empty"] + fx), b2=round(e / V["b2"]["empty"] + fx))))

    def carry_container(self, cname, frm, to, label, to_xy):
        e = self.leg(frm, False); c = self.leg(to, True)
        fx = T["container_pick"] + T["container_set"]
        self.add_time(e, c, fx, fx, containers=1)
        self.steps.append(dict(step=["carry", cname, {"to_scene": [round(float(v), 2) for v in to_xy], "to_world": [round(float(v), 2) for v in (np.asarray(to_xy) - START)]}],
                               what=label, runs_today=False, needs="NEW step type: carry a container with two hands (not built)",
                               walk_empty_m=round(e, 2), walk_carry_m=round(c, 2),
                               est_s=dict(stated=round(e / V["stated"]["empty"] + c / V["stated"]["carry"] + fx), b2=round(e / V["b2"]["empty"] + c / V["b2"]["carry"] + fx))))

    def deliver(self, names, dest_point, label, pairs=True):
        """Trips for the listed things to one place: nearest available thing next, a second one in the other hand when
        it is within 3 m of the first and goes to the same place (the runner's rule)."""
        todo = [OBJ[n] for n in names if OBJ[n].planned and n not in self.removed]
        order = []; t_stated = t_b2 = e_tot = c_tot = 0.0
        while todo:
            av = [o for o in todo if available(o, self.removed)]
            if not av:
                self.deferred += [o.name for o in todo]; break
            a = min(av, key=lambda o: walk(self.pos, o.name))
            trip = [a]
            if pairs and not is_single(a):
                c2 = [o for o in av if o is not a and not is_single(o) and o.dest == a.dest and np.linalg.norm(o.c[:2] - a.c[:2]) < 3.0]
                if c2:
                    trip.append(min(c2, key=lambda o: walk(a.name, o.name) + walk(o.name, dest_point)))
            e = self.leg(trip[0].name, False); c = 0.0
            for o in trip[1:]:
                c += self.leg(o.name, True)
            c += self.leg(dest_point, True)
            fs = sum(pick_time(o, "stated") + put_time(o, "stated") for o in trip); fb = sum(pick_time(o, "b2") + put_time(o, "b2") for o in trip)
            self.add_time(e, c, fs, fb, n_items=len(trip))
            ts = e / V["stated"]["empty"] + c / V["stated"]["carry"] + fs; tb = e / V["b2"]["empty"] + c / V["b2"]["carry"] + fb
            t_stated += ts; t_b2 += tb; e_tot += e; c_tot += c
            for o in trip:
                o.est = dict(today_stated_speeds_s=round(ts / len(trip)), today_run_B2_rates_s=round(tb / len(trip)), target_s=list(TARGET_ITEM),
                             trip_items=[x.name for x in trip], trip_walk_empty_m=round(e, 2), trip_walk_carry_m=round(c, 2), order_in_route=len(self.trips) + 1)
                self.removed.add(o.name); todo.remove(o); order.append(o.name)
            self.trips.append([o.name for o in trip])
        if not order:
            return
        kinds = {("cloth" if n in CLOTH else ("floor" if OBJ[n].rest["type"] == "floor" else "surface")) for n in order}
        dk = OBJ[order[0]].dest
        if kinds == {"floor"}:
            proven = dk == TOY
            step = ["tidy_all", {"names": order, "pairs": bool(pairs)}]
            needs = ("runs with today's runner" if proven else {MAT: "runner form exists; put_down on the flat mat with a target spot per shoe is NOT run yet (pair spots need a new option)",
                     RUB: "runner form exists; drop_in into the bin ran in the practice room only", CORNER: "runner form exists; needs a per-object destination spot on the floor (new option)",
                     SINK: "runner form exists but tidy_all skips destinations on furniture: place-into-sink is NOT BUILT",
                     CON: "runner form exists but tidy_all skips destinations on furniture: place_on is NOT BUILT",
                     ENTRY: "runner form exists; put_down on a per-object floor spot (room_patch_v3 target spot) is written, a flat floor destination not run yet",
                     BOXW: "runner form exists; a 25 cm tall box taken by its top ridge (top_down, 0.6 kg with the hold) and put down on a per-object floor spot: not run yet",
                     HAM: "runner form exists; drop_in into the hamper (rim 0.65 m)"}.get(dk, "destination not served yet"))
        elif kinds == {"cloth"}:
            step = ["garments", order]; needs = "the CLOTH agent's runner form (E:/urc_cloth/scripts/home/cloth_episode.py); one merged runner for cloth + rigid in the same episode does not exist yet"
        else:
            step = ["tidy_surface", {"names": order, "pairs": bool(pairs)}]
            needs = "NEW step type: pick from furniture (surface_pick) + " + DEST[dk]["put"] + "; floor and cloth things in the list go through their own skills"
        self.steps.append(dict(step=step, what=label, runs_today=bool(kinds == {"floor"} and dk == TOY and all(OBJ[n].grasp.get("type") == "top_down" for n in order)), needs=needs,
                               grasp_types=dict(collections.Counter(OBJ[n].grasp.get("type") for n in order)), destination=DEST[dk]["name"], n_items=len(order), n_trips=None,
                               walk_empty_m=round(e_tot, 2), walk_carry_m=round(c_tot, 2), est_s=dict(stated=round(t_stated), b2=round(t_b2))))


def names_to(dk, where=None):
    return [o.name for o in PLAN if o.dest == dk and (where is None or where(o))]


def build_route(bring_basket=True, bring_bin=True):
    S = Sim()
    east = lambda o: o.c[0] > 0.0
    west = lambda o: o.c[0] <= 0.0
    # 0 (v3) small floor things lying on or next to the new places of the big things go to their own places first
    pre = [o.name for o in PLAN if o.name not in BIG and o.rest["type"] == "floor" and hasattr(o, "rect")
           and any(float(r.dist(fp_points(o.rect.c, o.rect.h, o.rect.yaw)).min()) < 0.25 for r in PLACED)]
    for dk in dict.fromkeys(OBJ[n].dest for n in pre):
        S.deliver([n for n in pre if OBJ[n].dest == dk], "dest:" + dk, f"v3: clear the new places of the big things first ({DEST[dk]['name']})")
    # 1 (v3) the big things first: they stand in walking routes. Nearest first from where the robot is; one whose take
    #   stance needs neighbours gone waits and is tried again after every block below
    big_todo = [n for n in BIG if OBJ[n].planned]

    def try_big():
        while True:
            av = [n for n in big_todo if set(OBJ[n].reach.get("clear_first") or []) <= S.removed]
            if not av:
                return
            n = min(av, key=lambda n_: walk(S.pos, n_))
            S.big(OBJ[n], f"v3: {n} to {DEST[OBJ[n].dest]['name']} by {BIG[n]['method']} (it stands in a walking route)"); big_todo.remove(n)
    S.try_big = try_big
    try_big()
    _deliver = S.deliver

    def deliver_then_big(*a, **k):
        _deliver(*a, **k); try_big()
    S.deliver = deliver_then_big
    # 2 east half (the robot starts there): rubbish to the bin while it stands at home
    S.deliver(names_to(RUB, east), "dest:" + RUB, "east: rubbish to the bin (bin at home)")
    # 3 garments off the entry floor and the mat (this frees the mat and the console), the rag and the knit hat; v3: the towel off the stool
    S.deliver(names_to(HAM, lambda o: o.c[0] > -1.0), "dest:" + HAM, "entry, kitchen, hall: garments to the hamper (big ones one per trip, two hands); v3: the towel from the stool")
    # 4 shoes of the east half to the mat, in pairs; v3: the small umbrella by the front door
    S.deliver(names_to(MAT, east), "dest:" + MAT, "east: shoes to the doormat in pairs")
    S.deliver(names_to(ENTRY, lambda o: o.name not in BIG), "dest:" + ENTRY, "v3: the small umbrella to the floor by the front door")
    S.deliver(names_to(CON, east), "dest:" + CON, "entry: small things to the console table")
    # 5 kitchen: dishes to the sink, cleaning (and v3: laundry) things to the tray table, v3: the tote to the bags
    if DW_CLOSE and names_to(SINK):
        S.close_dw()
    S.deliver(names_to(SINK, east), "dest:" + SINK, "kitchen: used dishes from the island and the counter to the sink")
    S.deliver(names_to(TRAY, east), "dest:" + TRAY, "kitchen: cleaning things (and v3: the iron) from the island to the tray table")
    S.deliver(names_to(BAGS), "dest:" + BAGS, "v3: the tote from the island to the standing bags by the entry")
    # 6 crossing west: the toys of the east half ride along to the toy basket; v3: the cable bundle to the TV cabinet
    S.deliver(names_to(TOY, east), "dest:" + TOY, "crossing west: the east half's toys ride along to the toy basket at its home")
    S.deliver(names_to(TVTOP), "dest:" + TVTOP, "v3: crossing west: the cable bundle from the island to the TV cabinet")
    S.deliver(names_to(TOY, lambda o: o.c[0] < -3.9), "dest:" + TOY, "toy corner: toys near the basket's home into it")
    # 7 (v3) living room: the box to the wall (the TV-cabinet door is closed after the rug toys: its stance is among them)
    S.deliver(names_to(BOXW), "dest:" + BOXW, "v3: the cardboard box square against the wall")
    # 6 living room: basket to the rug toys, fill it, carry it back
    rug = [n for n in names_to(TOY, west) if n not in S.removed]
    if bring_basket and rug:
        POINTS_HOME = "dest:" + TOY
        S.carry_container("r186i1_basket", POINTS_HOME, "spot:basket_at_rug", "carry the toy basket to the rug toys", BASKET_AT_RUG)
        S.deliver(rug, "spot:basket_at_rug", "rug and side table: toys into the basket standing on the rug")
        S.carry_container("r186i1_basket", "spot:basket_at_rug", POINTS_HOME, "carry the full toy basket back to its place", DEST[TOY]["xy"])
    else:
        S.deliver(rug, "dest:" + TOY, "rug and side table: toys to the basket at its home (two per trip)")
    for n_ in DOOR_STEPS:                                   # (v3) the TV-cabinet door the pack leaves open, 0.5 m into the room
        S.close_door(n_, f"v3: close {n_} (open in the pack, standing {DOORS[n_]['sticks_out_m']['pack']:.2f} m out on average; its stance is free once the rug toys are gone)")
    S.deliver(names_to(CORNER), "dest:" + CORNER, "rug: the two big toys (v3: and the stick) to the toy corner (one per trip)", pairs=False)
    S.deliver(names_to(HAM, lambda o: o.c[0] <= -1.0), "dest:" + HAM, "rug: remaining garments to the hamper (v3: the strap, the coat from the armchair)")
    # 7 living-room rubbish
    lr = [n for n in names_to(RUB, west) if n not in S.removed]
    if bring_bin and lr:
        S.carry_container("rubbish_bin", "dest:" + RUB, "spot:bin_at_living", "carry the bin to the living room", BIN_AT_LIVING)
        S.deliver(lr, "spot:bin_at_living", "living room: rubbish into the bin standing there")
        S.carry_container("rubbish_bin", "spot:bin_at_living", "dest:" + RUB, "carry the bin back to its place by the wall", BIN["xy"])
    else:
        S.deliver(lr, "dest:" + RUB, "living room: rubbish to the bin at its home (two per trip)")
    # 8 things that leave the living room for the east half: nearest destination first, two per trip
    S.deliver(names_to(CON, west), "dest:" + CON, "living room: small things to the console table")
    S.deliver(names_to(MAT, west), "dest:" + MAT, "living room: the pair of flats to the doormat")
    S.deliver(names_to(ISL), "dest:" + ISL, "living room: food and drink to the kitchen island")
    S.deliver(names_to(SINK, west), "dest:" + SINK, "living room: used dishes to the sink (two per trip, the long way)")
    # 9 anything that was waiting for a neighbour
    for _ in range(3):
        d_ = [n for n in dict.fromkeys(S.deferred) if n not in S.removed]; S.deferred = []
        for dk in dict.fromkeys(OBJ[n].dest for n in d_):
            S.deliver([n for n in d_ if OBJ[n].dest == dk], "dest:" + dk, f"left-overs that waited for a neighbour: to {DEST[dk]['name']}")
    try_big()
    S.never = [n for n in dict.fromkeys(S.deferred) if n not in S.removed] + [n for n in big_todo if n not in S.removed]
    return S


ALT = {}
for bb in (True, False):
    for bn in (True, False):
        for o in PLAN:
            o.est = None
        s_ = build_route(bb, bn)
        ALT[(bb, bn)] = s_
best_key = min(ALT, key=lambda k: ALT[k].t["b2"])            # by what today's code really does end to end
for o in PLAN:
    o.est = None
ROUTE = build_route(*best_key)

# ---------------------------------------------------------------- write full_plan.json
def r2(v):
    return None if v is None else [round(float(x), 3) for x in v]


def clean(x):
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return [round(float(v), 3) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return float(x) if isinstance(x, np.floating) else int(x)
    return x


BOOK_STACK = {"r136i1_book": dict(stack_at="r135i1_side_table", order_bottom_to_top=["r136i1_book", "r136i2_book"], note="already stacked like this; left"),
              "r136i2_book": dict(stack_at="r135i1_side_table", order_bottom_to_top=["r136i1_book", "r136i2_book"], note="already stacked like this; left"),
              "r162i1_books": dict(stack_at="r159i1_cabinet", order_bottom_to_top=["r162i1_books"], note="a stack of its own on the TV cabinet; left. If all books were ever put on one pile: r136i2 (30 x 27 cm) at the bottom, r136i1 (28 x 24), r162 (27 x 22) on top; flat books cannot be taken by the jaws from a table top")}
done = [o for o in MESS if o.name in ROUTE.removed]
skipped = [o for o in MESS if o.name not in ROUTE.removed]
tot = ROUTE.t
GT_COUNT = collections.Counter(o.grasp.get("type") for o in done)
IMPOSSIBLE = sorted([o for o in MESS if o.grasp["verdict"] == "no"], key=lambda q: q.name)
SENS_PATH = os.path.join(HERE, "reach_sensitivity.json")   # read only in v3 (v2's sensitivity runs)
if DRY:
    rec = dict(reach=[REACH_YES, REACH_MARGINAL], dishwasher_closed=DW_CLOSE, planned=len(done), skipped=len(skipped), by_type=dict(GT_COUNT),
               not_reachable=sum(1 for o in skipped if o.grasp["verdict"] != "no"), generated=time.strftime("%Y-%m-%d %H:%M"))
    print("DRY (v3 writes nothing in this mode)", rec)
    for s_ in ROUTE.steps:
        print("  STEP", json.dumps(clean(s_["step"]))[:260], "|", s_["what"][:90], "|", s_["est_s"])
    print("  skipped:", [(o.name, (o.skip or "never reached")[:90]) for o in skipped])
    print("  times", {k: round(v) for k, v in tot.items()}, "trips", len(ROUTE.trips), f"{time.time() - T0:.0f} s"); sys.exit(0)
SENS = json.load(open(SENS_PATH, encoding="utf-8")) if os.path.exists(SENS_PATH) else {}
# ---- what a different hand would add (COARSE, geometry only): Unitree Dex3-1, three fingers
DEX3_SPAN = 0.143   # m: widest thumb-to-index/middle gap (closest surfaces), Menagerie G1-with-hands model (Dex3-1), searched over the thumb's joints


def dex3_coarse(o):
    if o.name in CLOTH:
        return True, "cloth"
    h = float(o.phi[2] - o.plo[2]); w = o.g.get("side_w") or 9.0
    if (o.mass or 0) > MASS_NO:
        return False, f"{o.mass:.1f} kg: the arm's limit, not the hand's"
    if h < 0.010:
        return False, f"{100 * h:.1f} cm flat: fingertips have no nail and no suction; only a slide to a table edge (same as the two jaws)"
    if w <= DEX3_SPAN - 0.01:
        return True, f"narrowest silhouette {100 * w:.0f} cm fits the {100 * DEX3_SPAN:.1f} cm span (wrap or three-finger pinch)"
    return False, f"narrowest silhouette {100 * w:.0f} cm: over the {100 * DEX3_SPAN:.1f} cm span"


DEX3 = {o.name: dex3_coarse(o) for o in MESS}
DEX3_NEW = [o for o in IMPOSSIBLE if DEX3[o.name][0]]
DEX3_EASIER = [o for o in MESS if o.grasp["verdict"] == "marginal" and DEX3[o.name][0] and any(k in o.grasp.get("why", "") for k in ("to spare a side", "pitch the hand", "swing", "turns it"))]
SUMMARY_DONE = True
entries = []
for o in sorted(FREE, key=lambda q: q.name):
    e = dict(name=o.name, id=o.id, cls=o.cls, mass_kg=o.mass, size_m=r2(o.size), position_m=r2(o.c), z_low_m=round(float(o.lo[2]), 3),
             rests_on=dict(o.rest, band=band(o.rest["surface_height_m"])), status=o.status, reason=o.reason)
    gi = dict(o.grasp)
    e["graspable"] = gi
    e["graspable_v1"] = o.grasp_v1
    if o.status == "mess_to_move":
        e["dex3_coarse"] = dict(graspable=DEX3[o.name][0], why=DEX3[o.name][1], basis="coarse, geometry only (object size vs the hand's span)")
    if o.name in BOOK_STACK:
        e["stack"] = BOOK_STACK[o.name]
    if o.status == "mess_to_move":
        sp = dest_spot(o); D = DEST[o.dest]
        e["destination"] = dict(key=o.dest, name=D["name"], kind=D["kind"], target_spot_scene=None if sp["xy"] is None else [round(float(sp["xy"][0]), 2), round(float(sp["xy"][1]), 2), sp["z"]],
                                target_spot_world=None if sp["xy"] is None else [round(float(sp["xy"][0] - START[0]), 2), round(float(sp["xy"][1] - START[1]), 2), sp["z"]],
                                note=sp.get("note"), pair_with=sp.get("pair_with"))
        e["skill"] = skills_of(o)
        e["reachable"] = o.reach
        e["planned"] = bool(o.planned and o.name in ROUTE.removed)
        e["skip_reason"] = o.skip if not o.planned else (None if o.name in ROUTE.removed else "never became reachable in the route (its neighbours could not be cleared)")
        e["estimate_s"] = o.est if (o.planned and getattr(o, "est", None)) else None
    else:
        e["destination"] = None; e["skill"] = None; e["reachable"] = None; e["planned"] = False; e["skip_reason"] = None; e["estimate_s"] = None
        if o.name in ("r186i1_basket", "rubbish_bin"):
            e["skill"] = dict(container_carry=True, needs_two_hands=True, pick_status="NOT BUILT (two hands on opposite walls)")
    entries.append(e)
out = dict(
    title="Apartment 1122: full tidy plan (planning only; every reach and grasp judgement is by geometry, not verified in simulation)",
    generated=time.strftime("%Y-%m-%d %H:%M"), generator=os.path.join(HERE, "make_full_plan_v3.py").replace("\\", "/"), logic=LOGIC,
    frame="scene frame of the pack (metres, Z up). Episode world frame = scene - (0.90, 0.45)",
    assumptions=dict(seconds=T, speeds_m_per_s=V, target_item_s=TARGET_ITEM, mass_limit_kg=MASS_NO, mass_marginal_kg=MASS_MARGINAL, open_jaws_m=OPEN_GAP, widest_section_m=W_YES,
                     surface_reach_yes_m=REACH_YES, surface_reach_marginal_m=REACH_MARGINAL, top_grasp_max_top_m=TOP_GRASP_MAX_Z, pelvis_to_furniture_m=R_BODY, pelvis_to_small_things_m=R_FOOT),
    counts=dict(free_objects=len(FREE), by_status=dict(collections.Counter(o.status for o in FREE)), mess_planned=len(done), mess_skipped=len(skipped),
                planned_by_grasp_type=dict(GT_COUNT), mess_with_no_grasp=len(IMPOSSIBLE), dex3_coarse_more_graspable=len(DEX3_NEW)),
    version="v3 'looks clean': v2 + the big floor things (carry2 / drag with forces against the hold's limits), towel and coat as cloth, strap, stick, kitchen things, open doors closed, big things first, clean_targets_v3.json",
    reach_map=dict(source=REACH_MAP["source"] if REACH_MAP else None, levels=REACH_MAP["levels"] if REACH_MAP else None,
                   used="MEASURED where the map has the height" if REACH_MAP else "ASSUMED limits (no measured map named in PROGRESS_CLOTH.md yet)",
                   assumed=dict(yes_m=REACH_YES, marginal_m=REACH_MARGINAL), sensitivity=SENS),
    dishwasher=dict(closed_in_plan=DW_CLOSE, closing_step_stances=DW_INFO, sink_variants=SINK_VARIANTS, sink_collider=SINK_COLLIDER),
    impossible_two_jaw=[dict(name=o.name, cls=o.cls, why=o.grasp["why"], by_type=o.grasp.get("why_not_by_type")) for o in IMPOSSIBLE],
    destinations=DEST_INFO,
    container_spots=dict(toy_basket_at_rug_scene=r2(BASKET_AT_RUG), bin_in_living_room_scene=r2(BIN_AT_LIVING)),
    objects=entries,
    route=dict(chosen=dict(bring_toy_basket_to_rug=best_key[0], bring_bin_to_living_room=best_key[1]),
               alternatives_s_stated_speeds={f"basket_to_rug={k[0]},bin_to_living={k[1]}": round(v.t["stated"]) for k, v in ALT.items()},
               steps=ROUTE.steps, trips=ROUTE.trips, never_reached=ROUTE.never,
               walk_empty_m=round(ROUTE.m_empty, 1), walk_carry_m=round(ROUTE.m_carry, 1),
               total_s=dict(today_stated_speeds=round(tot["stated"]), today_run_B2_rates=round(tot["b2"]), target_20s_per_item=round(tot["target_lo"]), target_30s_per_item=round(tot["target_hi"]))))
out_bin = dict(name="rubbish_bin", id="extra", cls="bin", mass_kg=1.5, size_m=BIN["size"], position_m=[1.0, 1.93, 0.2], z_low_m=0.0, rests_on=dict(type="floor", support="floor", surface_height_m=0.0, band="floor"),
               status="our_addition", reason="the added rubbish bin (not one of the pack's 198 loose objects); destination of the rubbish", graspable=None, destination=None,
               skill=dict(container_carry=True, needs_two_hands=True, pick_status="NOT BUILT (two hands on opposite walls)"), reachable=None, planned=False, skip_reason=None, estimate_s=None)
out["added_objects"] = [out_bin]
KITCHEN = sorted([o for o in FREE if o.rest["type"] != "floor" and o.c[0] > 1.7 and 0.85 < o.lo[2] < 1.25], key=lambda q: (q.rest["support"], q.name))


def v3_status(o):
    if o.status == "mess_to_move":
        if o.name in ROUTE.removed:
            sp_ = dest_spot(o)
            return "moved", f"to {DEST[o.dest]['name']}" + (f" at ({sp_['xy'][0]:.2f}, {sp_['xy'][1]:.2f})" if sp_.get("xy") is not None and o.dest not in (TOY, RUB, HAM, SINK) else "")
        return "NOT tidied", o.skip or "never became reachable in the route"
    if o.status == "mess_but_left":
        return "NOT tidied (left on purpose)", o.reason
    return "in place", o.reason


out["v3"] = dict(
    big_things={n_: dict(method=b_["method"], physics=b_["physics"], place=V3_SPOT.get(n_), search=V3_SEARCH.get(n_), reach=OBJ[n_].reach, planned=n_ in ROUTE.removed) for n_, b_ in BIG.items()},
    placed=V3_SPOT, searches=V3_SEARCH, umbrella_choice=UMB_CHOICE,
    doors=dict(open_in_pack=OPEN_DOORS, all=DOORS, close_steps=DOOR_STEPS, dishwasher="v2's close_dishwasher step (racks in, door up)"),
    soft_things={n_: dict(zip(("status", "why"), v3_status(OBJ[n_]))) for n_ in ("r100i1_towel", "r165i1_coat", "r144i1_cushion", "r144i2_cushion", "r144i3_cushion")},
    cords_and_strap={n_: dict(zip(("status", "why"), v3_status(OBJ[n_]))) for n_ in ("r198i1_cord", "r198i2_cord", "r194i1_strap")},
    kitchen={o.name: dict(support=o.rest["support"], **dict(zip(("status", "why"), v3_status(o)))) for o in KITCHEN},
    fridge=dict(shelf_used_z=FRIDGE_FLOOR_Z, shelf_heights_z=sorted(set(FRIDGE_FLOOR_HIT)), note="hollow in the collision model with shelf colliders (vertical rays, doors open); OPTIONAL round, needs the door skill"),
    not_clean_at_the_end=[dict(name=o.name, cls=o.cls, why=v3_status(o)[1]) for o in sorted(FREE, key=lambda q: q.name) if v3_status(o)[0].startswith("NOT")],
    hold_limits=dict(f_max_N=HOLD_F_MAX, t_max_Nm=HOLD_T_MAX), times_big_s=T_BIG)
json.dump(clean(out), open(os.path.join(HERE, "full_plan_v3.json"), "w", encoding="utf-8"), indent=1)
json.dump(clean([s["step"] for s in ROUTE.steps]), open(os.path.join(HERE, "route_steps_v3.json"), "w", encoding="utf-8"), indent=1)
# what the room file would need (to be merged by the floor agent; this script does not touch E:\urc_home)
room_patch = dict(note="Merge into the room JSON (structure.free, destinations). Display names of the pack. Spots are scene frame; the runner works in world = scene - (0.90, 0.45).",
                  free_add=sorted({o.name for o in done} | {"r186i1_basket", "r133i1_laundry_basket"}),
                  cloth=[n for n in CLOTH if n in ROUTE.removed],
                  destinations={o.name: DEST[o.dest]["name"] for o in done},
                  target_spots_scene={o.name: (clean(dest_spot(o)["xy"]) + [dest_spot(o)["z"]] if dest_spot(o)["xy"] is not None else None) for o in done},
                  target_spots_world={o.name: ([round(float(dest_spot(o)["xy"][0] - START[0]), 3), round(float(dest_spot(o)["xy"][1] - START[1]), 3), dest_spot(o)["z"]]
                                               if dest_spot(o)["xy"] is not None else None) for o in done},
                  grasp_type={o.name: o.grasp.get("type") for o in done},
                  grasp_candidate_scene={o.name: o.grasp.get("candidate") for o in done if o.grasp.get("candidate")},
                  hollow_colliders=dict(file=os.path.join(HERE, "hollow_colliders.json").replace("\\", "/"), apply_to=sorted(HOLLOW["bodies"]),
                                        needed_by_planned=sorted(o.name for o in done if o.grasp.get("type") == "rim_pinch" or o.name in HOLLOW["bodies"]),
                                        how="make_hollow_colliders.apply_to_body(el, entry) per body element"),
                  extras_add=[SINK_COLLIDER],
                  optional_step_unfreeze_joints=["r32i1_door", "r33i1_rack", "r33i2_rack"] if DW_CLOSE else [],
                  dishwasher="closed by the optional step close_dishwasher (route_steps.json)" if DW_CLOSE else "left open",
                  feet_may_step_on=WALK_OVER_THIN,
                  reach_map=REACH_MAP["source"] if REACH_MAP else "none named in PROGRESS_CLOTH.md yet: ASSUMED limits",
                  shoe_pairs=[list(p) for p in PAIRS])
room_patch.update(
    note_v3="v3 additions: the big things, the towel / coat as cloth (PROPOSED patterns), the TV-cabinet door and the dishwasher joints unfrozen, target poses with yaw for things placed on the floor.",
    cloth_new_proposed=dict(names=CLOTH_V3_NEW, how="as the 7 garments (structure.cloth): the towel one flat panel 53 x 49 cm (0.6 kg), the coat the jacket pattern at 52 x 65 cm (1.1 kg); "
                                                     "they lie on furniture (stool r99i2 seat 0.61 m, armchair r164i1): lay() must drape them over it, not on the floor"),
    unfreeze_joints=sorted(set((["r32i1_door", "r33i1_rack", "r33i2_rack"] if DW_CLOSE else []) + list(DOOR_STEPS))),
    open_doors_in_pack={n_: dict(q_in_pack=DOORS[n_]["q_in_pack"], q_closed=DOORS[n_]["q_closed"], joint=DOORS[n_]["joint"]) for n_ in OPEN_DOORS},
    placed_targets_scene={n_: dict(xy=[round(float(v_["xy"][0]), 3), round(float(v_["xy"][1]), 3)], z=v_["z"], yaw_deg=v_["yaw_deg"], footprint=v_["footprint"], against=v_["against"])
                          for n_, v_ in V3_SPOT.items() if n_ in ROUTE.removed},
    placed_targets_world={n_: [round(float(v_["xy"][0] - START[0]), 3), round(float(v_["xy"][1] - START[1]), 3), v_["z"], v_["yaw_deg"]] for n_, v_ in V3_SPOT.items() if n_ in ROUTE.removed},
    big_methods={n_: dict(method=b_["method"], recommended=b_["physics"].get("recommended")) for n_, b_ in BIG.items()},
    hold_limits=dict(f_max_N=HOLD_F_MAX, t_max_Nm=HOLD_T_MAX, source="urc.tasks.home.hold.Hold defaults"))
json.dump(clean(room_patch), open(os.path.join(HERE, "room_patch_v3.json"), "w", encoding="utf-8"), indent=1)

# ---------------------------------------------------------------- clean_targets_v3.json: what "looks clean" means, per loose thing (read by check_clean_look.py)
CONTAINERS = {
    "r186i1_basket": dict(movable=True, body="object_" + OBJ["r186i1_basket"].id.split("_")[1] + "_body", lo_off=None, hi_off=None),
    "rubbish_bin": dict(movable=True, body="rubbish_bin", start_scene=[float(BIN["xy"][0]), float(BIN["xy"][1]), 0.0], lo_off=[-0.15, -0.15, 0.0], hi_off=[0.15, 0.15, 0.45]),
    "r133i1_laundry_basket": dict(movable=True, body="r133i1_laundry_basket", start_scene=[float(OBJ["r133i1_laundry_basket"].c[0]), float(OBJ["r133i1_laundry_basket"].c[1]), 0.0105],
                                  lo_off=[-0.235, -0.235, 0.0], hi_off=[0.235, 0.235, 0.70]),
    "r27i1_sink": dict(movable=False, rect_scene=dict(c=[float(SINK_R["c"][0]), float(SINK_R["c"][1])], h=[float(SINK_R["h"][0]), float(SINK_R["h"][1])], yaw_deg=45.0), z=[0.66, 0.95]),
}
_bk = OBJ["r186i1_basket"]; _bkb = d.xpos[m.body(_bk.id + "_body").id]
CONTAINERS["r186i1_basket"].update(body=_bk.id + "_body", start_scene=[float(v) for v in _bkb], lo_off=[float(v) for v in (_bk.plo - _bkb + np.array([0.01, 0.01, -0.01]))],
                                   hi_off=[float(v) for v in (_bk.phi - _bkb + np.array([-0.01, -0.01, 0.10]))])
SURF = {}
for sup_ in ("r94i1_tray_table", "r159i1_cabinet", "r110i1_console", "r35i1_top", "r119i1_mat"):
    q_ = OBJ[sup_]
    SURF[sup_] = dict(lo_scene=[float(q_.lo[0]), float(q_.lo[1])], hi_scene=[float(q_.hi[0]), float(q_.hi[1])], z=[float(q_.hi[2]) - 0.04, float(q_.hi[2]) + 0.35])
DEST_TO_CONT = {TOY: "r186i1_basket", RUB: "rubbish_bin", HAM: "r133i1_laundry_basket", SINK: "r27i1_sink"}
DEST_TO_SURF = {TRAY: "r94i1_tray_table", TVTOP: "r159i1_cabinet", CON: "r110i1_console", ISL: "r35i1_top"}
CT = {}
for o in sorted(FREE, key=lambda q: q.name):
    bid_ = m.body(o.id + "_body").id; bp_ = d.xpos[bid_]; bq_ = d.xquat[bid_]
    e_ = dict(body=o.id + "_body", cls=o.cls, mass_kg=o.mass, cloth=o.name in CLOTH, start_scene=[round(float(v), 4) for v in bp_], start_quat_wxyz=[round(float(v), 5) for v in bq_],
              start_world=[round(float(bp_[0] - START[0]), 4), round(float(bp_[1] - START[1]), 4), round(float(bp_[2]), 4)], status_v3=o.status)
    if o.status == "mess_to_move" and o.name in ROUTE.removed:
        sp_ = dest_spot(o); dk_ = o.dest
        if dk_ in DEST_TO_CONT:
            e_["expect"] = dict(kind="in_container", container=DEST_TO_CONT[dk_])
        elif dk_ in DEST_TO_SURF:
            e_["expect"] = dict(kind="on_surface", surface=DEST_TO_SURF[dk_], spot_scene=None if sp_["xy"] is None else [round(float(v), 3) for v in sp_["xy"]])
        elif dk_ == MAT and sp_["xy"] is not None and "beside the mat" not in (sp_.get("note") or ""):
            e_["expect"] = dict(kind="on_surface", surface="r119i1_mat", spot_scene=[round(float(v), 3) for v in sp_["xy"]])
        else:
            yaw_ = sp_.get("yaw_deg")
            e_["expect"] = dict(kind="at_spot", spot_scene=[round(float(sp_["xy"][0]), 3), round(float(sp_["xy"][1]), 3)],
                                spot_world=[round(float(sp_["xy"][0] - START[0]), 3), round(float(sp_["xy"][1] - START[1]), 3)],
                                tol_xy_m=0.20 if dk_ == UMBW else (0.15 if dk_ in (PARK, BOXW, BAGS, ENTRY) else 0.25),
                                yaw_deg=yaw_ if dk_ in (PARK, BOXW, BAGS) else None, tol_yaw_deg=25.0, upright_max_tilt_deg=20.0 if dk_ in (PARK, BAGS, BOXW) else None)
        e_["expect"]["planned_by"] = "route_steps_v3.json"
    elif o.status == "mess_to_move":
        e_["expect"] = dict(kind="known_mess", why=o.skip or "never reached in the route", tol_xy_m=0.05)
    elif o.status == "mess_but_left":
        e_["expect"] = dict(kind="known_mess", why=o.reason, tol_xy_m=0.05)
    else:
        e_["expect"] = dict(kind="stay", why=o.reason, tol_xy_m=0.05, tol_z_m=0.05, max_tilt_change_deg=10.0)
    CT[o.name] = e_
CT["rubbish_bin"] = dict(body="rubbish_bin", cls="bin", mass_kg=1.5, cloth=False, start_scene=[float(BIN["xy"][0]), float(BIN["xy"][1]), 0.0], start_quat_wxyz=[1, 0, 0, 0],
                         start_world=[round(float(BIN["xy"][0] - START[0]), 4), round(float(BIN["xy"][1] - START[1]), 4), 0.0], status_v3="our_addition",
                         expect=dict(kind="stay", why="the added bin stands back at its place by the wall (it may be carried and brought back)", tol_xy_m=0.10, tol_z_m=0.05, max_tilt_change_deg=10.0))
clean_targets = dict(title="Apartment 1122: what 'looks clean' means for every loose thing (plan v3). Every judgement by geometry, not verified.",
                     generated=time.strftime("%Y-%m-%d %H:%M"), generator=os.path.join(HERE, "make_full_plan_v3.py").replace("\\", "/"),
                     frame="scene frame of the pack; world (episode) = scene - (0.90, 0.45); positions are body origins (= the free joint's qpos)",
                     start_offset_scene=[float(START[0]), float(START[1])], containers=CONTAINERS, surfaces=SURF,
                     kinds=dict(in_container="the body origin inside the container's box (movable containers: at the container's END pose)",
                                on_surface="the body origin over the surface's footprint and within its top band (z)", at_spot="within tol_xy_m of the spot (and yaw / upright when given)",
                                stay="within tol of its start pose and not tipped (tilt change)", known_mess="the plan cannot tidy it: counted as NOT clean while it is out of place"),
                     open_doors=[dict(name=n_, joint=DOORS[n_]["joint"], q_closed=DOORS[n_]["q_closed"], q_in_pack=DOORS[n_]["q_in_pack"]) for n_ in OPEN_DOORS],
                     objects=CT)
json.dump(clean(clean_targets), open(os.path.join(HERE, "clean_targets_v3.json"), "w", encoding="utf-8"), indent=1)

# ---------------------------------------------------------------- FULL_PLAN.md
def fmt_t(s):
    return f"{s / 60:.0f} min" if s < 5400 else f"{s / 3600:.1f} h"


L = []
A = L.append
A("# Apartment 1122: full tidy plan for one continuous episode")
A("")
A(f"Generated {out['generated']} by `{out['generator']}` (rerun: `py -3.12` on that file, about {time.time() - T0:.0f} s).")
A("**Nothing in this file is a simulation result.** Every reach and grasp judgement is by geometry, not verified. Coordinates are the pack's scene frame; the episode's world frame is scene - (0.90, 0.45).")
A("")
A("## v3 \"looks clean\" in short (v2 is kept as it was: FULL_PLAN.md, full_plan.json, route_steps.json, room_patch.json)")
_notc = out["v3"]["not_clean_at_the_end"]
A(f"- **{len(done)} things are planned in ONE route** (v2: 48), out of {len(MESS)} things counted as mess in v3 (v2: 69 + the big things, the towel, the coat, the strap, the stick and kitchen things). "
  f"{len(_notc)} loose things stay NOT clean at the end (list at the end of this section, each with the reason). Every method and reach judgement is by geometry, not verified.")
A(f"- The big things go FIRST (they stand in walking routes): {', '.join(s['step'][1] for s in ROUTE.steps if s['step'][0] in ('carry2', 'drag'))}; before them only the small things lying where the scooters will be parked "
  f"({', '.join(n for s in ROUTE.steps[:3] if s['step'][0] in ('tidy_all', 'tidy_surface') for n in s['step'][1]['names'])}).")
A(f"- New step types (runner form, route_steps_v3.json): `[\"carry2\", name, {{to_scene, to_world, grip, take_stance_scene, set_down, ...}}]`, `[\"drag\", name, {{to_scene, grip_point_scene, ...}}]`, "
  f"`[\"close_door\", name, {{joint, q_closed, push_point_scene, push_dir, stand_scene}}]`; the floor / surface / cloth things use the existing `tidy_all` / `tidy_surface` / `garments` with per-object spots (room_patch_v3.json).")
A(f"- Time: **{fmt_t(tot['stated'])}** with the stated speeds, **{fmt_t(tot['b2'])}** at run B2's end-to-end rates, {fmt_t(tot['target_lo'])} to {fmt_t(tot['target_hi'])} at the 20-30 s target "
  f"(big things: carry2 take {T_BIG['carry2_take']:.0f} s + set {T_BIG['carry2_set']:.0f} s, drag {T_BIG['drag_take']:.0f} + {T_BIG['drag_release']:.0f} s, close a door {T_BIG['close_door']:.0f} s: ASSUMED).")
A("")
A("### The big floor things: method, forces at the hand, place (by geometry, not verified)")
A(f"Hold limits used (urc.tasks.home.hold.Hold defaults): {HOLD_F_MAX:.0f} N force, {HOLD_T_MAX} N m torque; past them the held thing is pulled out of the hold. Friction: MuJoCo mixes the larger of the two "
  "geoms' values (scooters 0.8 on floor 0.6 / rug 0.85). The pack's bodies are single rigid bodies with no wheel joints: they slide, they do not roll; their centre of mass is the middle of their box.")
A("")
A("| Thing | kg | recommended | hand load | upright drag | tilted drag | place (scene x, y, yaw) | against | extra walking |")
A("|---|---|---|---|---|---|---|---|---|")
for n_, b_ in BIG.items():
    ph_ = b_["physics"]; sp_ = V3_SPOT.get(n_, {}); se_ = V3_SEARCH.get(n_, {}); best_ = se_.get("best") if "best" in se_ else (se_.get("anywhere") or {}).get("best")
    if b_["method"] == "carry2":
        load_ = f"{ph_['carry2']['per_hand_N']} N + {ph_['carry2']['per_hand_torque_Nm']} N m a hand"
        up_ = f"no: needs {ph_['drag_upright']['hand_torque_needed_Nm']} N m"; ti_ = f"{ph_['drag_tilted']['verdict']}: {ph_['drag_tilted']['hand_force_N']} N one hand" if "drag_tilted" in ph_ else "-"
        rec_ = "carry2 (both hands on the handlebar)"
    else:
        load_ = f"{ph_['drag_by_edge']['hand_force_N']} N"; up_ = "-"; ti_ = "-"; rec_ = "drag by the rim (far rim sliding)"
    A(f"| {n_} | {ph_['mass_kg']} | {rec_} | {load_} | {up_} | {ti_} | ({sp_.get('xy', [0, 0])[0]:.2f}, {sp_.get('xy', [0, 0])[1]:.2f}, {sp_.get('yaw_deg')} deg) | "
      f"{', '.join(sp_.get('against', [])[:2])} | {(best_ or {}).get('extra_walk_m_mean_per_pair', '-')} m |")
A("")
for n_, b_ in BIG.items():
    A(f"- {n_}: {b_['physics'].get('why_recommended')}. Place: {V3_SPOT.get(n_, {}).get('note')}. Take: {OBJ[n_].reach.get('why') if OBJ[n_].reach else '-'}"
      + (f"; set-down stance {OBJ[n_].reach.get('set_down')}" if OBJ[n_].reach and OBJ[n_].reach.get('set_down') else ""))
_us = V3_SEARCH.get("r106i1_umbrella", {})
A(f"- The open umbrella by the entry: the best place there ({((_us.get('by_the_entry') or {}).get('best') or {}).get('centre')}) adds {((_us.get('by_the_entry') or {}).get('best') or {}).get('extra_walk_m_mean_per_pair')} m "
  f"of walking per key pair (it narrows the only way past the stroller); the chosen place adds {((_us.get('anywhere') or {}).get('best') or {}).get('extra_walk_m_mean_per_pair')} m. Chosen: {UMB_CHOICE}. "
  "Its collider is a flat 3 cm slab (the dome is drawn only), so it cannot be stood up or closed; there is no handle in physics.")
A("- The toy bike r128i1 already stands along the hall wall beside the robot vacuum: it is the west end of the vehicle corner and is not moved.")
for n_ in ("r107i1_umbrella", "r175i1_cardboard_box", "r70i1_tote"):
    A(f"- {n_}: {v3_status(OBJ[n_])[0]}: {v3_status(OBJ[n_])[1]}; " + (V3_SPOT.get(n_, {}).get("note") or "") + f"; method: {OBJ[n_].grasp.get('type')} grasp ({OBJ[n_].grasp.get('verdict')}), {skills_of(OBJ[n_])['put']}")
A("- Two-hand carry for boxes: the cardboard box is 0.6 kg with a top ridge the jaws can take (top-down section 4.6-5.2 cm): one hand + the contact-verified hold; a push (0.6 x 5.9 = 3.5 N, below 0.23 m or it tips) is the fallback.")
A("")
A("### Soft things, cushions, cords and the strap")
for n_, v_ in list(out["v3"]["soft_things"].items()) + list(out["v3"]["cords_and_strap"].items()):
    A(f"- {n_}: {v_['status']}: {v_['why']}")
A(f"- Cloth proposal (room_patch_v3.json cloth_new_proposed): {room_patch['cloth_new_proposed']['how']}. The towel is in the first garments step (cloth pick from the stool's seat: NOT built); the coat's armchair is in the cut-off south-west corner.")
A("")
A("### The kitchen: every thing on the island and the counters")
A("| Thing | on | v3 | why / where |")
A("|---|---|---|---|")
for n_, v_ in out["v3"]["kitchen"].items():
    A(f"| {n_} | {v_['support']} | {v_['status']} | {v_['why']} |")
A(f"- The fridge compartment is hollow in the collision model (upward surfaces found by vertical rays, doors open: {sorted(set(FRIDGE_FLOOR_HIT))} m; the one used: {FRIDGE_FLOOR_Z} m): the milk jug (and the drinks on the island) go there in an OPTIONAL round once a door skill exists: "
  "open r34i1_fresh_door, place_on the compartment floor, close it. The island drawers r36i1-3 are hollow too (18 cm deep): snacks and the cable bundle could go in with a drawer skill. Neither is in the route.")
A("")
A("### Doors")
A(f"- Open in the pack (by geometry: the leaf / rack sticks out of its housing at q = 0): {', '.join(OPEN_DOORS)}. Everything else (front door, closets, cabinets, drawers, oven, fridge, lift-top, ottoman lid) is closed.")
A("- The dishwasher (door + 2 racks): v2's `close_dishwasher` step, before the first sink trip (the surface agent is building it).")
for n_, v_ in DOOR_STEPS.items():
    A(f"- {n_} (TV cabinet door, {DOORS[n_]['mass_kg']} kg, hinge {v_['hinge_scene']}): `close_door`, push at {v_['push_point_scene']} toward {v_['push_dir']}, stand at {v_['stand_scene']} "
      f"({v_['reach']}: {v_['reach_why']}); {v_['force_note']}. Before the rug toys (it stands 0.5 m into the room beside them).")
A("")
A("### What stays NOT clean at the end of this plan, and why")
for e_ in _notc:
    A(f"- {e_['name']} ({e_['cls']}): {e_['why']}")
A("")
A("## In v2's layout, with the v3 numbers")
A(f"- **{len(done)} of the {len(MESS)} mess things are planned** (v1: 25). By grasp type (by geometry, not verified; the live agents confirm or reject each NEW type): "
  + ", ".join(f"{k} {GT_COUNT[k]}" for k in ("top_down", "cloth", "side", "surface_pinch", "rim_pinch", "edge") if GT_COUNT[k]) + ".")
A(f"- {len(IMPOSSIBLE)} mess things have no grasp of any of the five types (list below: what remains impossible with a two-jaw gripper, and why); {len(skipped) - len([o for o in skipped if o.grasp['verdict'] == 'no'])} more have a grasp but no standing place within reach, a destination that cannot be reached, or no free target spot.")
A(f"- The sink decides most of the rest: {sum(1 for o in skipped if o.dest == SINK and o.grasp['verdict'] != 'no')} dishes with a grasp wait for it. Its nearest standing place is {DEST_INFO[SINK]['stand_dist_m']} m from the basin with the dishwasher closed "
  f"({DEST_INFO[SINK]['reach']} under the {REACH_MARGINAL} m limit; it would be marginal under v1's 0.60 m) and {SINK_VARIANTS['dishwasher open (as the pack is), feet may step on the scraps']['dist_m']} m with it open. "
  "The measured furniture reach map (cloth/surface agent) settles it; the corner cabinet's 12 cm bottom panel, which sticks out 25 cm in front of its diagonal face, is what keeps the robot away (see 'The sink and the dishwasher').")
A("- New in v2: five grasp types from the collision and visual meshes (grasps_v2.json, grasp_types.py, README_GRASPS.md); hollow colliders for 16 cups / glasses / bowls / mugs "
  "(hollow_colliders.json: the pack's colliders are solid hulls, so no rim pinch is possible without them); a collider for the SINK (the pack's sink has none: a dish let go over it falls into the cabinet); "
  "the dishwasher closed as an OPTIONAL step (sink stance computed both ways); a target spot for every planned thing (basket and sink slots too); a hook that reads a MEASURED reach map once the cloth/surface agent names one in PROGRESS_CLOTH.md "
  f"({'used: ' + REACH_MAP['source'] if REACH_MAP else 'none named yet: the ASSUMED limits are used, ' + str(REACH_YES) + ' m without a lean / ' + str(REACH_MARGINAL) + ' m with one'}).")
A("- v1's own outputs predate the previous agent's last edit of make_full_plan.py (a tight 7.8 cm section fallback and reach limits 0.34 / 0.50 m instead of 0.45 / 0.60 m): part of the change from v1 comes from that, not from the new grasp types. "
  + ("Reach sensitivity (same v2 code, other limits): " + "; ".join(f"{k}: {v['planned']} planned" for k, v in SENS.items()) + "." if SENS else ""))
A("")
A("## Counts")
st = collections.Counter(o.status for o in FREE)
A(f"- Loose objects in the pack: {len(FREE)} (+ our added rubbish bin).")
A(f"- Mess to move: {st['mess_to_move']} ({len(done)} planned in the route, {len(skipped)} skipped). Mess left on purpose: {st['mess_but_left']}. Already in place: {st['already_in_place']}. Furniture, appliances and things where they belong: {st['leave']}.")
A("")
A("| Class | all | mess planned | mess skipped | left / in place |")
A("|---|---|---|---|---|")
for c, n in sorted(collections.Counter(o.cls for o in FREE).items(), key=lambda kv: -kv[1]):
    A(f"| {c} | {n} | {sum(1 for o in done if o.cls == c)} | {sum(1 for o in skipped if o.cls == c)} | {sum(1 for o in FREE if o.cls == c and o.status != 'mess_to_move')} |")
A("")
A("| Destination | planned | skipped | where the robot stands / reach (by geometry, not verified) |")
A("|---|---|---|---|")
for k, D in DEST.items():
    di = DEST_INFO.get(k)
    A(f"| {D['name']} | {sum(1 for o in done if o.dest == k)} | {sum(1 for o in skipped if o.dest == k)} | {(di['reach'] + ': ' + di['reach_why']) if di else 'floor spots beside the toy basket'} |")
A("")
A("| Skill needed (planned things) | count | state today |")
A("|---|---|---|")
sk = collections.Counter(skills_of(o)["pick"] for o in done)
for k in ("floor_pick", "cloth_pick", "surface_pick"):
    o_ = next((o for o in done if skills_of(o)["pick"] == k), None)
    A(f"| {k} | {sk[k]} | {skills_of(o_)['pick_status'] if o_ else '-'} |")
for b_, n in sorted(collections.Counter(skills_of(o)["surface_height_band"] for o in done if skills_of(o)["pick"] == "surface_pick").items()):
    A(f"| surface_pick, {b_} | {n} | not built |")
pkey = lambda o: f"{DEST[o.dest]['put']} -> {DEST[o.dest]['name']}" + (" (cloth)" if o.name in CLOTH else "")
pk = collections.Counter(pkey(o) for o in done)
for k, n in pk.items():
    o_ = next(o for o in done if pkey(o) == k)
    A(f"| put: {k} | {n} | {skills_of(o_)['put_status']} |")
A(f"| needs_two_hands | {sum(1 for o in done if skills_of(o)['needs_two_hands'])} | not built (big garments, things over 1 kg) |")
A(f"| container_carry | {sum(1 for s in ROUTE.steps if s['step'][0] == 'carry')} carries | not built |")
A(f"| door / drawer (OPTIONAL step close_dishwasher) | {1 if DW_CLOSE and any(o.dest == SINK for o in done) else 0} step | not built; frees the sink. The milk jug (fridge) is still left |")
gv = collections.Counter(o.grasp["verdict"] for o in MESS)
A("")
A(f"Grasp by geometry over the {len(MESS)} mess things: yes {gv['yes']}, marginal {gv['marginal']}, no {gv['no']}. Reach: "
  + ", ".join(f"{k} {v}" for k, v in collections.Counter(o.reach['verdict'] for o in MESS).items()) + ".")
A("")
A("## Grasp types (v2, by geometry, not verified)")
A("Exactly what each type assumes: README_GRASPS.md. Counts over the mess things: 'usable' = has a yes / marginal candidate of that type; 'planned with it' = the type the plan uses.")
A("")
A("| Grasp type | mess things it can take | planned with it | skill today |")
A("|---|---|---|---|")
for t in ("top_down", "side", "surface_pinch", "rim_pinch", "edge"):
    A(f"| {t} | {sum(1 for o in MESS if o.grasp.get('types', {}).get(t) in ('yes', 'marginal'))} | {GT_COUNT[t]} | {TYPE_SKILL[t]} |")
A(f"| cloth (7 garments) | {sum(1 for o in MESS if o.name in CLOTH)} | {GT_COUNT['cloth']} | {TYPE_SKILL['cloth']} |")
A("")
A("Planned with a NEW grasp type (the live agents confirm or reject these first):")
for o in sorted([q for q in done if q.grasp.get("type") not in ("top_down", "cloth")], key=lambda q: q.name):
    A(f"- {o.name} ({o.cls}): {o.grasp['type']}, {o.grasp['verdict']}: {o.grasp['why']}")
A("")
A("## What remains impossible with a two-jaw gripper, and why")
for o in IMPOSSIBLE:
    A(f"- {o.name} ({o.cls}, {o.rest['support']}): {o.grasp['why']}")
A("In short: things under 1 cm thick lying flat on the floor (paper scraps, scissors) give two vertical pads nothing to close on, and the floor has no edge to slide them to; "
  "things wider than 7.9 cm everywhere with no rim, flange or edge (the clementine net, the cap, the filled bowl) have no section the jaws span. A suction cup, a fingernail-like scoop or a wider hand would be needed.")
A("")
A("## The sink and the dishwasher")
A("- The pack's sink r27i1 has NO collider (0 collision pieces) and the countertop's collider has a hole over it: a dish let go over the basin falls through to the corner cabinet's bottom panel (0.12 m). "
  "room_patch.json `extras_add` holds a fixed, invisible 5-box basin (floor 0.668-0.68 m, walls to 0.88 m, turned 45 deg like the basin) for OUR merged model.")
A(f"- The OPTIONAL step `close_dishwasher` (push both racks in, lift the door; door / drawer skill NOT built; ASSUMED {T['close_dishwasher']:.0f} s) comes before the first sink trip. Where the robot would stand for it (today's floor, dishwasher open):")
for k_, v_ in DW_INFO.items():
    A(f"  - {k_}: stand at {v_['stand_at']}, hand {v_['dist_m']} m away: {v_['reach']} ({v_['why']})")
A("- Sink stance (nearest standing place to a point 6 cm inside the basin), by geometry, not verified:")
for k_, v_ in SINK_VARIANTS.items():
    A(f"  - {k_}: stand at {v_['stand_at']}, {v_['dist_m']} m to the basin: {v_['reach']}")
A(f"- The plan uses: dishwasher {'closed' if DW_CLOSE else 'open'}; the feet may step on the 0.5 cm paper scraps {', '.join(WALK_OVER_THIN)} (no grasp takes them; ASSUMED safe, like the cords and mats).")
A("")
A("## Reach: assumed limits, and the hook for the measured map")
if REACH_MAP:
    A(f"- MEASURED reach map in use: {REACH_MAP['source']} (levels: " + ", ".join(f"{z:.2f} m: {a:.2f} / {b:.2f} m" for z, (a, b) in REACH_MAP['levels'].items()) + "); heights it does not cover use the ASSUMED limits.")
else:
    A(f"- No measured furniture reach map is named in {PROGRESS_CLOTH} yet, so the ASSUMED limits are used: the hand reaches {REACH_YES} m from where the pelvis stands without a lean (0.34 m is measured for the standing drop, skills.DROP_X) and {REACH_MARGINAL} m with a trunk lean (assumed).")
A("- Hook: `measured_reach_map()` reads the newest existing JSON whose name contains 'reach' named in PROGRESS_CLOTH.md (rows z, x, y, err_xy, err_z, lean as scripts\\home\\live\\s10_reach_probe.py writes them; reached = err_xy <= 1 cm and |err_z| <= 1.5 cm). Re-run this script after it appears.")
if SENS:
    for k_, v_ in SENS.items():
        A(f"- Sensitivity, {k_}: {v_['planned']} planned ({v_['generated']}).")
A("")
A("## What a different hand would add (Unitree Dex3-1, coarse, geometry only)")
A(f"Using the same object geometry, a three-finger Dex3-1 (thumb + two fingers; widest thumb-to-finger gap {100 * DEX3_SPAN:.1f} cm, measured on the Menagerie G1-with-hands model) would make "
  f"**{len(DEX3_NEW)} more of the {len(MESS)} mess things graspable** ({', '.join(o.name for o in DEX3_NEW) or 'none'}): things up to about 13 cm across that no jaw section, rim or edge serves. "
  f"It would also turn {len(DEX3_EASIER)} marginal two-jaw grasps into comfortable ones (tight 7.7-7.8 cm fits, hand pitched down, things that swing from a rim or edge grip: {', '.join(o.name for o in DEX3_EASIER) or 'none'}). "
  f"It would not help the {sum(1 for o in IMPOSSIBLE if not DEX3[o.name][0])} that stay impossible ({', '.join(o.name for o in IMPOSSIBLE if not DEX3[o.name][0])}): flat things under 1 cm still need a nail, a scoop or suction, and the rest are wider than its span or too heavy for the arm. "
  "This is a COARSE estimate from object sizes and the hand's span (no finger kinematics, contacts or reach were checked); reach and the destination limits would still apply, so it is not a count of extra planned items.")
A("")
A("## Skipped mess, and why")
for o in sorted(skipped, key=lambda q: q.name):
    A(f"- {o.name} ({o.cls}, to {DEST[o.dest]['name']}): {o.skip or 'never became reachable in the route'}")
A("")
A("Mess left on purpose (no destination the robot can serve):")
for o in sorted([q for q in FREE if q.status == "mess_but_left"], key=lambda q: q.name):
    A(f"- {o.name}: {o.reason}")
A("")
A("Things that are planned but only reachable after a neighbour is gone (the route respects this):")
for o in sorted([q for q in done if q.reach.get("clear_first")], key=lambda q: q.name):
    A(f"- {o.name}: clear {', '.join(o.reach['clear_first'])} first")
A("")
A("Planned with a marginal grasp or reach (expect failures here first):")
for o in sorted([q for q in done if q.grasp["verdict"] == "marginal" or q.reach["verdict"] == "marginal"], key=lambda q: q.name):
    A(f"- {o.name}: " + "; ".join(x for x in ((("grasp: " + o.grasp["why"]) if o.grasp["verdict"] == "marginal" else ""), (("reach: " + o.reach["why"]) if o.reach["verdict"] == "marginal" else "")) if x))
A("")
A("## Route (one episode)")
A(f"Chosen: toy basket carried to the rug toys: {'yes' if best_key[0] else 'no'}; bin carried to the living room: {'yes' if best_key[1] else 'no'}. "
  "Whole-route time with the stated speeds for the four ways: " + "; ".join(f"basket {'carried' if k[0] else 'stays'}, bin {'carried' if k[1] else 'stays'}: {fmt_t(v.t['stated'])}" for k, v in ALT.items()) + ".")
A(f"Toy basket spot on the rug (scene): ({BASKET_AT_RUG[0]:.2f}, {BASKET_AT_RUG[1]:.2f}). Bin spot in the living room (scene): ({BIN_AT_LIVING[0]:.2f}, {BIN_AT_LIVING[1]:.2f}).")
A("")
A("| # | Step (runner form) | What | Items | Walk empty / carrying m | s (stated speeds) | Runs today? |")
A("|---|---|---|---|---|---|---|")
for i, s in enumerate(ROUTE.steps, 1):
    st_ = s["step"]; nm = st_[1]["names"] if isinstance(st_[1], dict) and "names" in st_[1] else (st_[1] if isinstance(st_[1], list) else [st_[1]])
    A(f"| {i} | `{st_[0]}` | {s['what']} | {len(nm) if st_[0] != 'carry' else st_[1]} | {s['walk_empty_m']} / {s['walk_carry_m']} | {s['est_s']['stated']} | {'YES' if s['runs_today'] else 'no: ' + s['needs']} |")
A("")
A("The exact step list (names in order, pairs adjacent) is in `route_steps.json`; per-object trips and seconds are in `full_plan.json`.")
A("Step forms: `tidy_all` is the floor agent's (E:\\urc_home\\scripts\\home\\episode.py); `garments` is the cloth agent's (E:\\urc_cloth\\scripts\\home\\cloth_episode.py). "
  "NEW step types this plan needs: `carry` (a container, two hands), `tidy_surface` (pick from furniture; place on a table, a counter, into the sink). "
  "Also needed in the runner: one episode that mixes rigid and cloth steps, a destination PER OBJECT with a target spot (the room file maps a class to one place; `room_patch.json` holds the per-object table), and two per trip across neighbouring destinations.")
A("")
A("## Time for the whole apartment")
n = len(done)
A(f"- Things moved: {n} in {len(ROUTE.trips)} trips, + {sum(1 for s in ROUTE.steps if s['step'][0] == 'carry')} container carries. Planned walking: {ROUTE.m_empty:.0f} m empty-handed, {ROUTE.m_carry:.0f} m carrying.")
A(f"- Today, with the stated speeds (0.45 m/s empty, 0.18 m/s carrying, pick 16 s, put-down 12 s) and the robot walking exactly the planned legs: **{fmt_t(tot['stated'])}** ({tot['stated'] / n:.0f} s a thing).")
A(f"- Today, at the end-to-end rates measured in run 1118_204943 (B2: 4.2 m of legs in 36 s empty, 7 m in 111 s carrying, pick 18 s, put-down 20 s): **{fmt_t(tot['b2'])}** ({tot['b2'] / n:.0f} s a thing). This is what the code as committed would do, if nothing failed.")
A(f"- At the target of 20-30 s a thing (container carries at 0.45 m/s on top): **{fmt_t(tot['target_lo'])} to {fmt_t(tot['target_hi'])}**.")
A("- Not in these numbers: failed grasps and second tries, falls, the scene settling at the start, compute time (the CPU path ran about 0.6x real time with recording).")
A("")
A("## Top risks")
RISKS = [
    "Most of the plan needs skills that do not exist: of the planned things only the floor toys into the toy basket use skills proven in a clean episode (one toy piece, 176 s). Surface picks, placing on tables / counters / into the sink, the container carry and the cloth pick are not built or not proven.",
    f"{sum(1 for o in done if o.grasp.get('type') not in ('top_down', 'cloth'))} planned things rely on a NEW grasp type (side, surface pinch, rim pinch, edge) that exists only as geometry; rim pinches also need the hollow colliders applied, edge grasps a slide skill when the thing does not overhang.",
    "The sink has no collider in the pack: until SINK_COLLIDER (room_patch.json extras_add) is in the room, every dish 'put in the sink' falls into the cabinet below.",
    "The living room is far from the kitchen: used dishes travel about 9-10 m each, two per trip. At today's carrying speed this is the largest block of time. A dish caddy (a movable box carried once) would cut it but needs two-hand carrying of about 2.5 kg, over the 1.5 kg limit; not planned.",
    "Reach onto furniture is ASSUMED (0.45 m from the pelvis, 0.60 m with a lean); no reach map exists for standing or half-squat picks at 0.45-0.95 m. Things in the middle of the island, at the back of the counter and on the window sills behind the armchair and the gold table depend on it.",
    "The sink is in the corner behind the open dishwasher door and racks; with the optional closing step: " + (DEST_INFO[SINK]["reach"] + ": " + DEST_INFO[SINK]["reach_why"]) + ". Four paper scraps lie on the floor exactly there and cannot be picked up (0.5 cm thin): the plan lets the feet step on them.",
    "The doormat is half covered by the floor lamp's base; only the free part is used for the shoes: " + "; ".join(f"{k}: {('(%.2f, %.2f)' % tuple(v['xy'])) if v['xy'] is not None else 'NO SPOT'}" for k, v in SPOT.items() if k in MOVE and MOVE[k] == MAT) + ".",
    "The toy basket is small (33 x 27 x 12 cm, about 10 litres) and already holds a plush: " + str(sum(1 for o in done if o.dest == TOY)) + " more toys are planned into it. It will be heaped; overflow goes into the megabloks bag beside it (TIDY_PLAN). Carrying a heaped basket can spill.",
    "Walking distances are planned on the floor as it is AFTER the mess is gone; early trips are a little longer. Things moved to their places (shoes on the mat, a basket on the rug) are not put back into the map as new obstacles.",
    "Garments: the cloth pick is assumed to work for all seven; the three big ones (jacket, coat pile 1.4 kg, blanket) are assumed to need both hands and one trip each. The coat pile is the first thing that must go: it covers the mat and blocks the console.",
    "Heavy or off-centre grasps are marked marginal (pad friction alone, 6 N a pad measured): clementines 1.0 kg, salad bowl 0.9 kg, dollhouse 0.8 kg, lysol 0.75 kg, light saber held off its middle.",
    "A one-hour-plus episode with 198 loose bodies is beyond what the simulator has run: the full loose set ran under 0.02x real time on the GPU path; the room file must keep only the planned things loose (`room_patch.json`).",
]
for r_ in RISKS:
    A(f"- {r_}")
A("")
A("## Assumptions (all of them)")
ASSUME = [
    "Source of truth for names, classes, masses, positions and sizes: D:\\apartment_real\\mujoco\\unzipped (scene_spec.json, environment.xml), read only. Grasp sections and footprints come from the collision meshes at their start poses (the light saber and the santa hat move a little when the scene settles).",
    f"Grasp (v2): five types from grasps_v2.json (README_GRASPS.md says what each assumes): top_down (the floor agent's search, unchanged, plus a tight 7.8 cm fallback marked marginal), side, surface_pinch, rim_pinch (with the hollow colliders), edge. Preference when several work: yes before marginal, then top_down, side, surface pinch, rim pinch, edge (floor: top_down, surface pinch, side, rim pinch); the reach step may pick another usable type when the preferred one has no standing place. Fingers-down grasps on furniture are marginal when the thing's top is over {TOP_GRASP_MAX_Z} m. The jaws open {100 * OPEN_GAP:.1f} cm between the pad faces in the model (the brief says 8.2 cm).",
    "Side and edge grasps on furniture: the robot must stand on the side the hand comes from (within 60 deg of the approach); an edge grasp's slide must be clear of things that stay; things in the way that are moved anyway make it 'after clearing'.",
    f"Mass: over {MASS_NO} kg not carried; {MASS_MARGINAL}-{MASS_NO} kg marginal.",
    "Garments (7) are cloth and count as graspable by a pinch; their rigid drape shapes are used only as footprints.",
    f"Floor reach: a pick stance as skills.stance_for builds it (thing 0.17 m ahead and 0.27 m to the side of the standing pelvis, pelvis {R_BODY} m from furniture and {R_FOOT} m from small things, knees 12 cm clear of anything over 15 cm, feet 4 cm clear of floor things, 12 headings, both hands), checked on a 5 cm grid. Cords, the strap and the mats are walked over, as in the floor agent's room file.",
    f"Furniture reach: the pelvis may stand 0.22 m from furniture; a grasp point within {REACH_YES} m of such a place counts as reachable, within {REACH_MARGINAL} m marginal. " + ("A MEASURED map is used where it has the height." if REACH_MAP else "ASSUMED: no measured map yet (hook: measured_reach_map())."),
    "Dishes on the coffee table, side table, two-tier table, sills, island and the right counter are taken as used and go to the sink; dishes in the open dishwasher racks, at the sink and beside the dish basket are taken as in place. The sink is assumed to take 16 small dishes.",
    "Flat papers on the sofa and the empty pouch are rubbish (TIDY_PLAN). Snack bags, the juice box, the chips can and the paper bag in the kitchen are food or storage, not rubbish.",
    "Books are already stacked and stay; the remote stays on the two-tier table; keyboard, mouse and notebook stay on the window sill (deviation from TIDY_PLAN's 'books and remote on the coffee table': nothing is gained by moving them and flat books cannot be grasped).",
    "Santa hat to the hamper and stocking to the toy basket, as TIDY_PLAN classes them.",
    "Cleaning things from the island go to the tray table beside the mop; the cap, scissors and small umbrella go to the console table (my choice of place; TIDY_PLAN names the console for scissors and umbrella).",
    "Doors, drawers and lids stay as they are (frozen in our model): nothing is put into the fridge, cabinets, drawers, the ottoman or the lift-top table. The one exception is the OPTIONAL close_dishwasher step (racks in, door up), which needs those 3 joints left free and a door / drawer skill; the dishes in its racks go in with them.",
    "Target spots: every planned thing has one (room_patch.json target_spots_scene / _world): shoes in pairs on the mat, free places on tables, slots in the toy basket (layered when full) and on the sink's basin floor (nearest the stance first), and a release point over the bin and the hamper. If the toy basket is carried to the rug, its slots move with it.",
    "Times: floor pick 16 s and put-down 12 s (run B) or 18 s and 20 s (run B2) are measured; cloth pick 30 s (45 s two hands), surface pick 20 s, drop into bin / hamper 8 s, into the sink 10 s, place on a table 12 s, container pick-up 25 s and set-down 15 s are GUESSES. A second thing in a trip costs its own pick and put. A trip's time is shared equally by its things.",
    "Route: the zone order is fixed by hand (east half first because the robot starts there and the coat pile must leave the mat first; then the crossing west with the east toys; the living room; last the things that leave the living room). Inside a block the nearest available thing is next and the second hand takes a thing within 3 m going to the same place (the runner's own rule). The four ways (basket carried or not, bin carried or not) are all computed and the fastest by the stated speeds is taken. Not a proven optimum.",
    "Things moved in one trip with two hands (big garments, anything over 1 kg) travel alone.",
]
for a_ in ASSUME:
    A(f"- {a_}")
A("")
A("## Files")
for f_ in ("full_plan_v3.json", "route_steps_v3.json", "room_patch_v3.json", "clean_targets_v3.json", "FULL_PLAN_v3.md", "make_full_plan_v3.py", "check_clean_look.py",
           "full_plan.json", "route_steps.json", "room_patch.json", "FULL_PLAN.md", "make_full_plan.py", "grasps_v2.json", "grasp_types.py", "make_grasps_v2.py", "README_GRASPS.md",
           "hollow_colliders.json", "make_hollow_colliders.py", "hollow_colliders_qc.png", "reach_sensitivity.json", "nav_snapshot.py", "grasp_geom_snapshot.py",
           "FULL_PLAN_v1.md", "full_plan_v1.json", "route_steps_v1.json", "room_patch_v1.json", "make_full_plan_v1.py"):
    A(f"- `{os.path.join(HERE, f_)}`")
open(os.path.join(HERE, "FULL_PLAN_v3.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"done in {time.time() - T0:.1f} s | free {len(FREE)} | mess {len(MESS)} planned {len(done)} skipped {len(skipped)} | route {len(ROUTE.steps)} steps, {len(ROUTE.trips)} trips | "
      f"today {fmt_t(tot['stated'])} (stated) / {fmt_t(tot['b2'])} (B2 rates) | target {fmt_t(tot['target_lo'])}-{fmt_t(tot['target_hi'])} | chosen {best_key}")
