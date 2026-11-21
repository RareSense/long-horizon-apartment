# SAVE GAME in a live session (AI-operated): checkpoints EVERYWHERE (user's rule, 19 Nov 15:00), on the library
# urc.tasks.home.savegame (save_ckpt / load_ckpt: the whole state, exact; format there). exec'd after episode.py's set-up.
#   - before every action: the skills' motion primitives are wrapped (walk, turns, crouch / stand, hand moves, jaws,
#     carry pose, basket moves...) and every leg of walk_path calls PRE_ACTION: a checkpoint "act" is saved first (once
#     per control step), with the action's name and arguments in meta.json info (a resume calls it again from there);
#   - rolling: every ROLL_S of sim time a checkpoint "roll" (inside an action: for replaying a failure frame by frame;
#     the skill's own call stack is not in it); only the last ROLL_KEEP are kept;
#   - item end: route.py saves one after every thing that ends ok, and then deletes the "act" and "roll" ones of that
#     thing (kept for the whole run: start and item ends).
#   ck_save(name, kind="item", info=None) / ck_load(path) / ck_list() / ck_disk()
import importlib as _il, json as _json, time as _time, shutil as _sh
import urc.tasks.home.savegame as SG
_il.reload(SG)

CK_DIR = os.path.join(RUN, "checkpoints")
os.makedirs(CK_DIR, exist_ok=True)
ROLL_S, ROLL_KEEP = 5.0, 20
CK_ON = True                                       # False: no automatic saves (a session only looking at a replay)
CK_LOG = globals().get("CK_LOG", [])
# the pieces of video this session recorded: one per load (from_ckpt, start_frame) with the checkpoints saved in it
# (name, frames); join_segments.py follows the chain of checkpoints back from the last one through these pieces
CK_PIECES = globals().get("CK_PIECES") or [dict(run=RUN, from_ckpt=(globals().get("SEG") or {}).get("from_ckpt"),
                                                start_frame=(globals().get("SEG") or {}).get("start_frame", 0), saves=[])]


def _pieces_write():
    _json.dump(CK_PIECES, open(os.path.join(RUN, "pieces.json"), "w"), indent=1, default=str)


def _git_info():
    import subprocess as _sp
    try:
        h_ = _sp.run(["git", "-C", r"E:\urc_home", "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20).stdout.strip()
        dirty_ = _sp.run(["git", "-C", r"E:\urc_home", "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20).stdout.strip()
        return dict(commit=h_, dirty=bool(dirty_), dirty_files=dirty_.splitlines()[:20])
    except Exception as ex:
        return dict(error=str(ex))


# what the session was built from (search agent's request): the USD Newton parsed and the code's git state when the
# session loaded (the code a resume must run is that commit; dirty files are listed)
CK_SESSION = globals().get("CK_SESSION") or dict(usd=(globals().get("SCN") or {}).get("usd"), git=_git_info(), textured=os.environ.get("URC_TEXTURED"))
CK_STATE = dict(last_k=-1, last_roll_k=int(br.k), item=None,
                n=1 + max([int(x[:4]) for x in os.listdir(CK_DIR) if os.path.isdir(os.path.join(CK_DIR, x)) and x[:4].isdigit()] or [-1]))   # numbers never reused


def ck_quiet():
    return SG.is_quiet(globals())


def ck_save(name, kind="item", info=None, look=True):
    """Save the whole state now as checkpoints\\NNN_<kind>_<name>. Returns the folder."""
    nn = CK_STATE["n"]; CK_STATE["n"] += 1
    safe = "".join(ch if ch.isalnum() or ch in "_-." else "_" for ch in str(name))[:60]
    path = os.path.join(CK_DIR, f"{nn:04d}_{kind}_{safe}")
    lk = (lambda p: snap(p, f"checkpoint {nn:04d} {kind} {name}")) if look else None
    info = dict(info or {})
    if "route" not in info and callable(globals().get("_route_state")):
        # EVERY checkpoint (item, act, roll) carries the route state as it is NOW (19 Nov: an act checkpoint had none, and
        # route_resume set POS 0 / DONE [] after loading one)
        try:
            info["route"] = _route_state()
        except Exception as ex:
            info["route_error"] = str(ex)[:120]
    meta = SG.save_ckpt(path, globals(), name=name, info=dict(info, kind=kind, item=CK_STATE["item"], session=CK_SESSION), look=lk)
    CK_STATE["last_k"] = int(br.k)
    if kind == "roll":
        CK_STATE["last_roll_k"] = int(br.k)
    CK_LOG.append(dict(t=round(float(d.time), 2), k=int(br.k), path=path, kind=kind, name=name, bytes=meta.get("bytes"), save_s=meta.get("save_s"), item=CK_STATE["item"]))
    CK_PIECES[-1]["saves"].append(dict(path=path, frames=meta.get("frames"), t=round(float(d.time), 3)))
    _pieces_write()
    if kind != "roll" and kind != "act":
        print(f"[checkpoint] {os.path.basename(path)} t={d.time:.2f} s, {meta.get('bytes', 0) / 1e6:.2f} MB, {meta.get('save_s')} s", flush=True)
    return path


def ck_load(path):
    meta = SG.load_ckpt(path, globals())
    CK_STATE.update(last_k=int(br.k), last_roll_k=int(br.k))
    # the "held" finger shape (lock_fingers) is made at run time in GRIP_SET and is not in a checkpoint: a fresh session
    # that loads a checkpoint taken while holding stopped with KeyError 'held' (19 Nov 19:30). Made again here from the
    # finger angles just loaded.
    if globals().get("HOLD") is not None and callable(globals().get("lock_fingers")):
        for s_ in SIDES:
            try:
                if HOLD.holding(s_):
                    lock_fingers(s_)
            except Exception as ex:
                print("[checkpoint] re-lock fingers", s_, ex, flush=True)
    r_ = globals().get("rec")
    if r_ is not None and getattr(r_, "fps", None) and getattr(r_, "dt", None):
        # the recorder's frame clock to the loaded step count: else it renders a frame at every step until it catches up
        # (cloth agent, 19 Nov) and the video gets a burst of frames
        r_.k0 = int(br.k - round(r_.n / r_.fps / r_.dt))
    CK_PIECES.append(dict(run=RUN, from_ckpt=path, start_frame=getattr(r_, "n", 0) if r_ is not None else 0, saves=[]))
    _pieces_write()
    print(f"[checkpoint] loaded {path}: t={d.time:.3f} s, k={br.k}, {meta.get('loaded')}", flush=True)
    return meta


def ck_list(kind=None):
    out = []
    for x in sorted(os.listdir(CK_DIR)):
        if kind is None or f"_{kind}_" in x:
            out.append(x)
    return out


def ck_prune_item(item=None):
    """After a thing ended ok: ITS 'act' and 'roll' checkpoints go (the item-end one stays; those of other items, e.g.
    a failed one moved to the end, stay: pruning all of them lost the scooter carry checkpoints, 19 Nov 16:40)."""
    n = 0
    item = item or CK_STATE["item"]
    for e in CK_LOG:
        if e.get("kind") in ("act", "roll") and e.get("pruned") is None and e.get("item") == item and os.path.isdir(e["path"]):
            if e.get("kind") == "act":
                # 20 Nov (coordinator): KEEP meta.json (the action and its args) so the episode can be replayed / audited;
                # only the heavy state files go
                for f_ in os.listdir(e["path"]):
                    if f_ != "meta.json":
                        try:
                            os.remove(os.path.join(e["path"], f_))
                        except OSError:
                            pass
            else:
                _sh.rmtree(e["path"], ignore_errors=True)
            e["pruned"] = True; n += 1
    return n


def ck_disk():
    tot = 0; nn = 0
    for x in os.listdir(CK_DIR):
        p_ = os.path.join(CK_DIR, x)
        if os.path.isdir(p_):
            nn += 1; tot += sum(os.path.getsize(os.path.join(p_, f)) for f in os.listdir(p_))
    return dict(n=nn, MB=round(tot / 1e6, 1))


def _ck_down():
    """Fallen, for the save game: NOT skills.fallen() (pelvis under 0.45 m), which is true in every deep squat (pelvis
    0.27-0.39 m): with it no checkpoint was saved during the grasps of run 1119_144818. Down = not finite, pelvis under
    0.20 m or the trunk tilted over 1.0 rad."""
    if not np.all(np.isfinite(d.qpos)):
        return True
    tor = m.body("torso_link").id
    return bool(d.qpos[2] < 0.20 or float(np.arccos(np.clip(d.xmat[tor][8], -1, 1))) > 1.0)


def _action_log(action, info, ck):
    """Every PRE_ACTION as one line of the run folder's actions.jsonl (sim time, recorder frame, action, args, checkpoint)."""
    try:
        r_ = globals().get("rec")
        row = dict(sim_t=round(float(d.time), 3), k=int(br.k), frame=getattr(r_, "n", None) if r_ is not None else None,
                   action=action, info=_short(info or {}), ckpt=os.path.basename(ck) if ck else None)
        with open(os.path.join(RUN, "actions.jsonl"), "a", encoding="utf-8") as f_:
            f_.write(_json.dumps(row) + "\n")
    except Exception as ex:
        print("[actions.jsonl]", str(ex)[:120], flush=True)


def PRE_ACTION(action, info=None):
    """Called before every action: a checkpoint unless one was saved at this very control step; always a line in
    actions.jsonl."""
    ck = None
    if CK_ON and int(br.k) != CK_STATE["last_k"] and not _ck_down():
        ck = ck_save(action, kind="act", info=dict(action=action, **(info or {})), look=False)
    _action_log(action, info, ck)
    return ck


def _short(v):
    try:
        if isinstance(v, np.ndarray):
            return np.round(v, 4).tolist()
        if isinstance(v, (list, tuple)) and len(v) < 12:
            return [_short(x) for x in v]
        if isinstance(v, dict):
            return {str(k): _short(x) for k, x in list(v.items())[:12]}
        if isinstance(v, (int, float, str, bool, type(None))):
            return v
        return repr(v)[:120]
    except Exception:
        return "?"


def _wrap_action(fname):
    f = globals().get(fname)
    if not callable(f) or getattr(f, "_ck_wrapped", False):
        return False

    def w(*a, **kw):
        PRE_ACTION(fname, dict(args=_short(list(a)), kwargs=_short(kw)))
        return f(*a, **kw)
    w._ck_wrapped = True; w.__name__ = fname; w.__doc__ = f.__doc__; w._inner = f
    globals()[fname] = w
    return True


ACTIONS = ("walk", "_turn_on_spot", "crouch", "crouch_holding", "stand_up", "stand_with", "servo_pads", "close_jaws", "open_jaws",
           "carry_pose", "rest_hands", "arms_to", "both_move", "park_hands", "stand_from_squat", "set_basket_down", "pick_into",
           "drop_in", "put_down", "lock_grip", "unlock_grip", "surface_posture", "squeeze_on", "sc_hands_to", "sc_close", "sc_hold",
           "sc_lift", "sc_set_down", "sc_release", "walk_to_stance")
CK_WRAPPED = [fn for fn in ACTIONS if _wrap_action(fn)]
if not getattr(op.move, "_ck_wrapped", False):
    _op_move0 = op.move

    def _op_move(*a, **kw):
        PRE_ACTION("hand_move", dict(args=_short(list(a)), kwargs=_short({k: v for k, v in kw.items() if k != "quats"})))
        return _op_move0(*a, **kw)
    _op_move._ck_wrapped = True
    op.move = _op_move

_ON_STEP0 = globals().get("_ON_STEP0") or br.on_step


def _on_step_roll():
    if _ON_STEP0 is not None:
        _ON_STEP0()
    if CK_ON and int(br.k) - CK_STATE["last_roll_k"] >= int(ROLL_S / 0.002) and not _ck_down():
        ck_save(f"t{float(d.time):.1f}", kind="roll", look=False)
        rolls = [e for e in CK_LOG if e.get("kind") == "roll" and not e.get("pruned") and os.path.isdir(e["path"])]
        for e in rolls[:-ROLL_KEEP]:
            _sh.rmtree(e["path"], ignore_errors=True); e["pruned"] = True


br.on_step = _on_step_roll
print("[checkpoint] save game on: before every action (", len(CK_WRAPPED), "primitives + walk legs + hand moves ), rolling every", ROLL_S, "s; folder", CK_DIR, flush=True)
