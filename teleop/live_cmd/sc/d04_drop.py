import time as _tm
MON["on"] = False
_w0 = _tm.time()
zz_b = body_of("r120i1_duck"); zz_cb = body_of("r186i1_basket")
lo_c, hi_c = obj_box(zz_cb)
inner_ = tuple(b2 for b2 in INFO["bodies"] if b2 not in (zz_b, zz_cb) and inside(b2, zz_cb))
mon_start(target=None); MON["held"][SD] = zz_b; MON["last_touch"][SD] = float(d.time)
MON["ignore_names"] = (zz_cb,) + inner_ + (body_of("r130i1_light_saber"),)
top_in = max([float(obj_box(b2)[1][2]) for b2 in inner_] + [float(hi_c[2])])
print("inner", [INFO["bodies"][b2].get("display") for b2 in inner_], "top_in", round(top_in, 3), flush=True)
o_ = {}
try:
    Q_ = {SD: q_(ts.ee_pose(SD)[1])}
    tgt_ = np.array([-5.16, -1.39])
    for hh_, ll_ in ((-0.20, 0.35), (-0.30, 0.6), (-0.38, 0.8)):
        PRE_ACTION("squat_put", dict(h=hh_, l=ll_)); squat_follow((SD,), hh_, ll_, T=1.4)
        hang_ = pad_mid(SD)[2] - obj_box(zz_b)[0][2]
        PRE_ACTION("hand_over", {}); e_ = servo_pads(SD, tgt_, top_in + 0.05 + hang_, Q_, speed=0.10, n=3)
        lo_o, hi_o = obj_box(zz_b); oc_ = (lo_o + hi_o) / 2
        over_ = bool(np.all(oc_[:2] > lo_c[:2] + 0.05) and np.all(oc_[:2] < hi_c[:2] - 0.05) and lo_o[2] > top_in)
        o_.update(err=np.round(e_, 3).tolist(), over=over_, squat=hh_, duck=np.round(oc_, 3).tolist())
        print("try", hh_, o_, flush=True)
        if over_: break
    if o_.get("over"):
        PRE_ACTION("let_go", {}); open_jaws(SD, T=0.3); MON["held"].pop(SD, None); HELD.pop(SD, None); op.run(1.0)
        hp_ = ts.ee_pose(SD)[0]
        op.move({SD: [hp_[0], hp_[1], hp_[2] + 0.08]}, speed=0.2, quats=Q_, timeout=3.0, tol=0.02)
    rest_hands((SD,))
    PRE_ACTION("stand_up", {}); crouch(-0.20, 0.35, T=1.2); stand_up()
except Abort as ex_:
    o_["abort"] = str(ex_)
MON["on"] = False
o_["inside"] = bool(inside(zz_b, zz_cb))
print("DROP", o_, "state", state(), "fell", fallen(), "duck", np.round(centre(zz_b), 3).tolist(), "wall", round(_tm.time() - _w0), flush=True)
print(close(os.path.join(LK, "d04_basket.jpg"), np.r_[-4.75, -1.0, 1.1], np.r_[-5.18, -1.40, 0.05], "basket"), flush=True)
print(look3("d04_duck_dropped"), flush=True)
