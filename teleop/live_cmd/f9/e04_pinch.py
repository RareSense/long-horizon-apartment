MON["on"] = False
ck_load(os.path.join(RUN, "checkpoints", "0182_item_r125i1_flat")); gait_on(); settle_after_load(); refresh_jointed_footprints()
print(floor_first(["r106i1_umbrella"])[:2], flush=True)
mon_start(target=None)
try:
    r_ = tmove(fwd=-0.12, tag="off_lamp"); print("back", r_["at"], r_["touch"]["body"], flush=True)
    r_ = tmove(side=-0.12, tag="off_lamp_w"); print("west", r_["at"], r_["touch"]["body"], flush=True)
except Abort as ex_:
    print("abort", ex_, flush=True)
MON["on"] = False
zz_pl = corner_pinch_plan(zz_u, 0, "right")[0]
zz_o = corner_pinch_try(zz_u, 0, "right", s_=0.035, z_=0.013, force=14.0, pick=zz_pl)
print("TRY", {k_: v_ for k_, v_ in zz_o.items() if not str(k_).startswith("look")}, flush=True)
print(look_hand("right", "umb_pinch"), flush=True)
