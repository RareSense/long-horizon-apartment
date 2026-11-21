ck_load(ZZ_CK); gait_on(); ts.loco.g["hold"] = False      # gait agent: hold OFF until its next commit (it corrects while turning)
# the knit hat's own walk put a foot on the light saber's east end; the saber pick failed (pads 5 cm above its grasp
# point): first to the open floor east of the knit hat by way points 0.35 m clear of the saber's east end and of the croc
mon_start(); MON["trace"] = []
zz_ok = True
try:
    walk_via([(-0.75, -1.12), (-0.80, -0.15)], seg=0.30)
except Abort as ex:
    zz_ok = False; print("PRE ABORT", ex)
MON["on"] = False
print("pre", zz_ok, state(), "trace", MON["trace"][::5][:20], flush=True)
MON["trace"] = None
if zz_ok:
    print("ckpt", ck_save("pre_knit_hat_ok", kind="act"))
    zz_gr = go_item()
