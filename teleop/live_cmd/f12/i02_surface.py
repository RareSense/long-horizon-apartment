def surf_item(nm):
    """Autonomous surface item (library tidy_surface, tight fallback), recorded on the chain when ok."""
    zz_b = body_of(nm); out_ = {}
    floor_first([nm])
    mon_start(target=zz_b)
    try:
        r_ = tidy_surface(zz_b, "auto")
        if r_.get("error") and "no place to stand" in str(r_.get("error")) and not (r_.get("picks") or [{}])[0].get("ok"):
            print("no stance -> tight", flush=True)
            r_ = with_tight(lambda: tidy_surface(zz_b, "auto"))
        out_ = r_
    except Abort as ex_:
        out_ = dict(ok=False, error="abort: " + str(ex_))
    except Exception:
        import traceback as _tb; out_ = dict(ok=False, error=_tb.format_exc()[-700:])
    MON["on"] = False
    print("TIDY", nm, {k_: v_ for k_, v_ in out_.items() if k_ not in ("puts", "picks")}, flush=True)
    print("picks", str(out_.get("picks"))[:500], flush=True)
    print("puts", str([{k_: v_ for k_, v_ in p_.items() if k_ != "walk"} for p_ in out_.get("puts", []) if isinstance(p_, dict)])[:600], flush=True)
    print("at", np.round(centre(zz_b), 3).tolist(), "held", {s_: grip_check(s_, zz_b).get("ok") for s_ in SIDES}, "state", state(), "fell", fallen(), flush=True)
    print(look3(f"f12_{nm}_end"), flush=True)
    return out_


ZZ = surf_item("r149i1_pouch")
