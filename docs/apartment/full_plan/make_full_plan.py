r"""Full tidy plan for Apartment 1122, v2 (planning only: NOTHING here is a simulation result).

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


for o in FREE:
    o.g = grasp_info(o)
    o.grasp_v1 = grasp_verdict_v1(o)
    o.grasp = grasp_verdict(o)

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
    if o.plo[2] > 0.25 or o.cls in ("cable", "rug") or not len(o.P):     # up on furniture / cords and mats are walked over (static and under 3 cm in the room file)
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


for o in FREE:
    o.reach, o.stand, o.grasp_used = None, None, None
    if o.status != "mess_to_move":
        continue
    if o.rest["type"] == "floor":
        o.reach, s = floor_reach(o)
        o.stand = None if s is None else s["xy"]
    else:
        o.reach, o.stand = surface_reach(o)
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


def dims(o):
    h = o.rect.h if hasattr(o, "rect") else None
    if h is None:
        c, h, _ = NAV.min_rect(o.P[:: len(o.P) // 400 + 1])
    return 2 * float(max(h)), 2 * float(min(h))               # long, short side of its footprint


SPOT = {}                                                  # name -> dict(xy, z, note)
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
# things set on furniture: a free place near the edge the robot can stand at
for dk, sup in ((CON, "r110i1_console"), (ISL, "r35i1_top"), (TRAY, "r94i1_tray_table")):
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
for n_ in ("r188i1_dollhouse", "r130i1_light_saber"):
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
    elif DEST_INFO.get(o.dest, {}).get("reach") == "no":
        o.planned, o.skip = False, f"its destination {DEST[o.dest]['name']} cannot be reached: {DEST_INFO[o.dest]['reach_why']}"
PLAN = [o for o in MESS if o.planned]


def skills_of(o):
    floor = o.rest["type"] == "floor"; D = DEST[o.dest]
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
                  CON: "NOT BUILT (place_on a table)", ISL: "NOT BUILT (place_on a counter)", TRAY: "NOT BUILT (place_on a table)"}[o.dest]
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
    if k in (TOY, CORNER, MAT):
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
                     CON: "runner form exists but tidy_all skips destinations on furniture: place_on is NOT BUILT"}.get(dk, "destination not served yet"))
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
    # 1 east half first (the robot starts there): rubbish to the bin while it stands at home
    S.deliver(names_to(RUB, east), "dest:" + RUB, "east: rubbish to the bin (bin at home)")
    # 2 garments off the entry floor and the mat (this frees the mat and the console), the rag and the knit hat
    S.deliver(names_to(HAM, lambda o: o.c[0] > -1.0), "dest:" + HAM, "entry, kitchen, hall: garments to the hamper (big ones one per trip, two hands)")
    # 3 shoes of the east half to the mat, in pairs
    S.deliver(names_to(MAT, east), "dest:" + MAT, "east: shoes to the doormat in pairs")
    S.deliver(names_to(CON, east), "dest:" + CON, "entry: small things to the console table")
    # 4 kitchen: dishes to the sink, cleaning things to the tray table
    if DW_CLOSE and names_to(SINK):
        S.close_dw()
    S.deliver(names_to(SINK, east), "dest:" + SINK, "kitchen: used dishes from the island and the counter to the sink")
    S.deliver(names_to(TRAY, east), "dest:" + TRAY, "kitchen: cleaning things from the island to the tray table")
    # 5 crossing west: the toys of the east half ride along to the toy basket
    S.deliver(names_to(TOY, east), "dest:" + TOY, "crossing west: the east half's toys ride along to the toy basket at its home")
    S.deliver(names_to(TOY, lambda o: o.c[0] < -3.9), "dest:" + TOY, "toy corner: toys near the basket's home into it")
    # 6 living room: basket to the rug toys, fill it, carry it back
    rug = [n for n in names_to(TOY, west) if n not in S.removed]
    if bring_basket and rug:
        POINTS_HOME = "dest:" + TOY
        S.carry_container("r186i1_basket", POINTS_HOME, "spot:basket_at_rug", "carry the toy basket to the rug toys", BASKET_AT_RUG)
        S.deliver(rug, "spot:basket_at_rug", "rug and side table: toys into the basket standing on the rug")
        S.carry_container("r186i1_basket", "spot:basket_at_rug", POINTS_HOME, "carry the full toy basket back to its place", DEST[TOY]["xy"])
    else:
        S.deliver(rug, "dest:" + TOY, "rug and side table: toys to the basket at its home (two per trip)")
    S.deliver(names_to(CORNER), "dest:" + CORNER, "rug: the two big toys to the toy corner (one per trip)", pairs=False)
    S.deliver(names_to(HAM, lambda o: o.c[0] <= -1.0), "dest:" + HAM, "rug: remaining garments to the hamper")
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
    S.never = [n for n in dict.fromkeys(S.deferred) if n not in S.removed]
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
SENS_PATH = os.path.join(HERE, "reach_sensitivity.json")
if DRY:
    rec = dict(reach=[REACH_YES, REACH_MARGINAL], dishwasher_closed=DW_CLOSE, planned=len(done), skipped=len(skipped), by_type=dict(GT_COUNT),
               not_reachable=sum(1 for o in skipped if o.grasp["verdict"] != "no"), generated=time.strftime("%Y-%m-%d %H:%M"))
    S_ = json.load(open(SENS_PATH, encoding="utf-8")) if os.path.exists(SENS_PATH) else {}
    S_[f"reach {REACH_YES} / {REACH_MARGINAL} m, dishwasher {'closed' if DW_CLOSE else 'open'}"] = rec
    json.dump(S_, open(SENS_PATH, "w", encoding="utf-8"), indent=1)
    print("DRY (nothing else written)", rec); sys.exit(0)
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
    generated=time.strftime("%Y-%m-%d %H:%M"), generator=os.path.join(HERE, "make_full_plan.py").replace("\\", "/"), logic=LOGIC,
    frame="scene frame of the pack (metres, Z up). Episode world frame = scene - (0.90, 0.45)",
    assumptions=dict(seconds=T, speeds_m_per_s=V, target_item_s=TARGET_ITEM, mass_limit_kg=MASS_NO, mass_marginal_kg=MASS_MARGINAL, open_jaws_m=OPEN_GAP, widest_section_m=W_YES,
                     surface_reach_yes_m=REACH_YES, surface_reach_marginal_m=REACH_MARGINAL, top_grasp_max_top_m=TOP_GRASP_MAX_Z, pelvis_to_furniture_m=R_BODY, pelvis_to_small_things_m=R_FOOT),
    counts=dict(free_objects=len(FREE), by_status=dict(collections.Counter(o.status for o in FREE)), mess_planned=len(done), mess_skipped=len(skipped),
                planned_by_grasp_type=dict(GT_COUNT), mess_with_no_grasp=len(IMPOSSIBLE), dex3_coarse_more_graspable=len(DEX3_NEW)),
    version="v2: five grasp types (grasps_v2.json), hollow colliders, sink collider + stance with the dishwasher closed (optional step), per-object target spots, measured-reach hook",
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
json.dump(clean(out), open(os.path.join(HERE, "full_plan.json"), "w", encoding="utf-8"), indent=1)
json.dump(clean([s["step"] for s in ROUTE.steps]), open(os.path.join(HERE, "route_steps.json"), "w", encoding="utf-8"), indent=1)
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
json.dump(clean(room_patch), open(os.path.join(HERE, "room_patch.json"), "w", encoding="utf-8"), indent=1)

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
A("## v2 in short (v1 is kept as FULL_PLAN_v1.md, full_plan_v1.json, route_steps_v1.json, room_patch_v1.json)")
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
for f_ in ("full_plan.json", "route_steps.json", "room_patch.json", "FULL_PLAN.md", "make_full_plan.py", "grasps_v2.json", "grasp_types.py", "make_grasps_v2.py", "README_GRASPS.md",
           "hollow_colliders.json", "make_hollow_colliders.py", "hollow_colliders_qc.png", "reach_sensitivity.json", "nav_snapshot.py", "grasp_geom_snapshot.py",
           "FULL_PLAN_v1.md", "full_plan_v1.json", "route_steps_v1.json", "room_patch_v1.json", "make_full_plan_v1.py"):
    A(f"- `{os.path.join(HERE, f_)}`")
open(os.path.join(HERE, "FULL_PLAN.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"done in {time.time() - T0:.1f} s | free {len(FREE)} | mess {len(MESS)} planned {len(done)} skipped {len(skipped)} | route {len(ROUTE.steps)} steps, {len(ROUTE.trips)} trips | "
      f"today {fmt_t(tot['stated'])} (stated) / {fmt_t(tot['b2'])} (B2 rates) | target {fmt_t(tot['target_lo'])}-{fmt_t(tot['target_hi'])} | chosen {best_key}")
