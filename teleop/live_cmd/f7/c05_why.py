for e_ in EVENTS[-14:]:
    print({k_: (str(v_)[:160]) for k_, v_ in e_.items()}, flush=True)
print([ (c_["name"], c_["t"]) for c_ in CK_LOG[-14:] if c_.get("kind") != "roll"], flush=True)
print("trace", MON.get("trace", [])[-30:], flush=True)
print("mat spots", DESC.get("spots", {}).get("r119i1_mat") if isinstance(DESC.get("spots"), dict) else None, flush=True)
