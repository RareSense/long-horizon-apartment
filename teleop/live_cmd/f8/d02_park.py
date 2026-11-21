MON["trace"] = []
zz_r = park_scooter_sofa("r126i1_scooter")
if zz_r.get("status") == "ERROR" and ("no free path" in str(zz_r.get("why")) or "no place to stand" in str(zz_r.get("why"))) and not zz_r.get("moves"):
    print("-> tight", str(zz_r.get("why"))[-200:], flush=True)
    zz_r = with_tight(lambda: park_scooter_sofa("r126i1_scooter"))
print("PARK", str({k_: v_ for k_, v_ in zz_r.items() if k_ not in ("moves", "grip_detail")})[:1800], flush=True)
print("moves", [(m_[0], m_[1], m_[2]) if isinstance(m_, tuple) else m_ for m_ in zz_r.get("moves", [])][:30], flush=True)
print("state", state(), "fell", fallen(), "touch", contact_report(), "kit", kit_mem(), flush=True)
