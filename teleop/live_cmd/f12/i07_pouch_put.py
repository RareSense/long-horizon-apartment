MON["on"] = False
o_ = {}
mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
try:
    PRE_ACTION("stand_with", {}); crouch_holding((SD,), H_WALK, 0.0, T=2.0)
    o_["after_stand"] = dict(lost=hold_lost(SD), at=np.round(centre(zz_b), 3).tolist())
    pts_ = put_away(zz_b, SD)
    o_["puts"] = str([{k_: v_ for k_, v_ in p_.items() if k_ != "walk"} for p_ in pts_ if isinstance(p_, dict)])[:700]
except Abort as ex_:
    o_["abort"] = str(ex_)[:300]
except Exception:
    import traceback as _tb; o_["error"] = _tb.format_exc()[-700:]
MON["on"] = False
o_.update(at=np.round(centre(zz_b), 3).tolist(), in_bin=inside(zz_b, body_of("rubbish_bin")), held=HOLD.holding(SD), state=state(), fell=fallen())
print("PUT", o_, flush=True)
print(look3("f12_pouch_put"), flush=True)
