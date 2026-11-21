MON["on"] = False
exec(open(r"E:\urc_fable3\scripts\home\island_skills.py", encoding="utf-8").read())
exec(open(r"E:\urc_fable3\scripts\home\table_skills.py", encoding="utf-8").read())
if "_slide_out0" not in globals():
    _slide_out0 = slide_out
def slide_out(*a, **k):
    k.setdefault("inset", 0.015)        # the stick is 3 cm wide: press 1.5 cm inside its near edge
    return _slide_out0(*a, **k)
sb_ = body_of("r154i1_stick")
tb_ = [bx for s_ in INFO["static"] if s_["name"] == "r145i1_lift_top" for bx in (s_.get("pieces") or s_["boxes"])]
print("table pieces", [(np.round(bx["c"], 2).tolist(), np.round(np.asarray(bx["s"]) / 2, 2).tolist()) for bx in tb_][:4], flush=True)
print("stick", [np.round(v_, 3).tolist() for v_ in obj_box(sb_)], flush=True)
mon_start(target=sb_)
try:
    zz_e = edge_pick(sb_, "right", (-4.55, float(centre(sb_)[1]), 0.0), slide=0.035, press=6.0, force=10.0, back=0.05)
except Abort as ex_:
    zz_e = dict(abort=str(ex_)[:300])
MON["on"] = False
print("EDGE", {k_: v_ for k_, v_ in zz_e.items() if k_ not in ("approach",)}, flush=True)
print("held", {s_: HOLD.holding(s_) for s_ in SIDES}, "stick", np.round(centre(sb_), 3).tolist(), "state", state(), "fell", fallen(), flush=True)
print(look3("f12_stick_edge"), flush=True)
