exec(open(r"E:\urc_scout\scripts\home\live\hall.py", encoding="utf-8").read())
LD = "0418_act_let_go"
MON["on"] = False
zz_m = route_v3_resume(os.path.join(RUN, "checkpoints", LD)); gait_on(); sync_cloth(force=True)
zz_b = body_of("r120i1_duck"); zz_cb = body_of("r186i1_basket")
print("loaded", state(), "held", HOLD.holding("left"), finger_touch("left", zz_b), flush=True)
mon_start(target=None); MON["held"]["left"] = zz_b; MON["last_touch"]["left"] = float(d.time)
inner_ = tuple(b2 for b2 in INFO["bodies"] if b2 not in (zz_b, zz_cb) and inside(b2, zz_cb))
MON["ignore_names"] = (zz_cb,) + inner_
try:
    release_and_stand(zz_b, "left", {"left": q_(ts.ee_pose("left")[1])}, up=0.08)
except Abort as ex_:
    print("ABORT", ex_, flush=True)
MON["on"] = False
print("after", state(), "fell", fallen(), "duck", np.round(centre(zz_b), 3).tolist(), "inside", inside(zz_b, zz_cb), flush=True)
print(look3("d11_release"), flush=True)
