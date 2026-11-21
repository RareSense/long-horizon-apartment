def zz_tmove(**kw):
    """tmove under the monitor; returns the record or the abort reason."""
    mon_start(target=None); MON["t_max"] = 600.0
    try:
        r_ = tmove(**kw)
    except Abort as ex_:
        r_ = dict(abort=str(ex_))
    MON["on"] = False
    return r_
