import inspect as _insp
print("squeeze" , hasattr(op, "squeeze"), "carry", hasattr(op, "carry"), "_hold_cmds", hasattr(op, "_hold_cmds"), flush=True)
print("walk_path sig", str(_insp.signature(walk_path))[:200], flush=True)
print("squeeze sig", str(_insp.signature(op.squeeze))[:300] if hasattr(op, "squeeze") else None, flush=True)
print("GG", "GG" in globals(), "NAV", "NAV" in globals(), "FINGER", "FINGER" in globals(), flush=True)
