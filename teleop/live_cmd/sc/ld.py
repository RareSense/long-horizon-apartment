# load a checkpoint of this run (or a full path) the standard way: resume, gait, cloth drawn, footprints, hands, settle
MON["on"] = False
_p = LD if os.path.isabs(LD) else os.path.join(RUN, "checkpoints", LD)
zz_m = route_v3_resume(_p); gait_on(); sync_cloth(force=True)
refresh_jointed_footprints(); rest_hands(SIDES)
op.run(4.0, until=_standing); op.run(1.5)
print("LOADED", _p, state(), "route head", [item_name(s_) for s_ in ROUTE[POS:POS + 3]], "done", len(DONE), flush=True)
