exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\final\n2\xlib.py", encoding="utf-8").read())
nm_ = "r195i1_paper"; pb_ = body_of(nm_); bn_ = body_of("rubbish_bin"); o_ = {}; CK_STATE["item"] = "fix_" + nm_
mon_start(target=pb_)
try:
    pk_ = with_tight(lambda: pick_floor(pb_, "auto"))
    o_["pick"] = {k_: pk_.get(k_) for k_ in ("ok", "side")}
except Abort as ex_:
    o_["abort_pick"] = str(ex_)[:300]
except RuntimeError as ex_:
    o_["err_pick"] = str(ex_)[:300]
MON["on"] = False
print("PICK", o_, flush=True)
x_report("x12_paper1_pft")
