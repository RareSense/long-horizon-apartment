(ck_load(os.path.join(RUN, "checkpoints", ZZ_CK)) if ZZ_CK else None); gait_on()
exec(open(r"C:/Users/raresense/sim_home/apartment/live_cmd/f10/e02_squeeze.py", encoding="utf-8").read().split("mon_start(target=pb_)")[0])
TWO["on"] = True
if ZZ_CK: TWO["vise"] = False; two_keep(4.0); two_keep(1.5)
bk_ = body_of("r186i1_basket"); h = op._hold; xy_ = np.array([-5.10, -1.36])
def zz_touch():
    return [c_ for c_ in _thing_contacts(pb_) if "Dex1" not in c_ and "wrist" not in c_]
print("loaded", state()["pelvis"], "pouch", np.round(centre(pb_), 3).tolist(), "saber", np.round(centre(body_of("r130i1_light_saber")), 3).tolist(), {s_: zz_force(s_) for s_ in SIDES}, flush=True)
mon_start(target=None); MON["held"] = {}; MON["ignore_names"] = tuple(b_ for b_ in INFO["bodies"] if b_ == pb_ or b_ == bk_ or inside(b_, bk_)); MON["ignore"] = {m.body(pb_).id}
zz_st = []
try:
    if ZZ_CK: two_reanchor(ride=False)
    TWO["vise"] = True; two_keep(0.5)
    S = dict(cz0=float(h["c_ref"][2]), pz0=float(base()[0][2]), dz=0.0, dz_goal=0.0)
    cmd = lambda: _two_track(pb_, xy_, S)
    op.run(4.0, [cmd])
    for hh_, ll_ in ZZ_STAGES:
        PRE_ACTION("two_hand_squat", dict(h=hh_, l=ll_)); op.send(dict(cmd="posture", height=hh_, lean=ll_, duration=2.5)); op.run(3.5, [cmd])
        zz_st.append((hh_, ll_, round(float(obj_box(pb_)[0][2]), 3), np.round(xy_ - centre(pb_)[:2], 3).tolist(), {s_: zz_force(s_) for s_ in SIDES}, zz_touch(), state()["pelvis"]))
        print("stage", zz_st[-1], flush=True)
        if zz_touch(): break
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
print(look3("pouch_lean"), flush=True)
