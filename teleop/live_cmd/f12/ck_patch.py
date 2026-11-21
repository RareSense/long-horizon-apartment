# Session patch (20 Nov, coordinator): keep act meta.json at prune; actions.jsonl for every PRE_ACTION. AI-operated.
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


print("[ck patch] prune keeps meta.json; actions.jsonl on", flush=True)
