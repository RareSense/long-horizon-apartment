nm = "r158i1_tissue"; tb_ = body_of(nm); SD = "right"; bn_ = body_of("rubbish_bin")
ck_load(os.path.join(RUN, "checkpoints", [c_ for c_ in sorted(os.listdir(os.path.join(RUN, "checkpoints"))) if c_.endswith("_act_n1_tissue_held")][-1])); gait_on(); op.run(0.5); refresh_jointed_footprints()
HELD[SD] = dict(min_gap=0.004)
print("RELOADED tissue_held rec", rec.n, "holding", HOLD.holding(SD), "bin", np.round(centre(bn_), 3).tolist(), [np.round(v_, 3).tolist() for v_ in obj_box(bn_)], flush=True)
mon_start(target=None); MON["held"][SD] = tb_; MON["last_touch"][SD] = float(d.time); MON["t_max"] = 900.0
o_ = {}
try:
    crouch_holding((SD,), H_WALK, 0.0, T=2.0)
    bc_ = centre(bn_)
    st_ = (float(bc_[0]) - 0.03, float(bc_[1]) - 0.40, np.pi / 2)
    globals()["CARRY_JOINTS"] = True
    w_ = walk_tight(st_, carry=(SD,))
    o_["walk"] = {k_: w_.get(k_) for k_ in ("ok", "err_xy")} if isinstance(w_, dict) else str(w_)[:200]
except (Abort, RuntimeError) as ex_:
    o_["abort"] = str(ex_)[:300]
finally:
    globals()["CARRY_JOINTS"] = False
MON["on"] = False
print("CARRY", o_, "state", state(), "held", HOLD.holding(SD), "tissue", np.round(centre(tb_), 3).tolist(), "touch", contact_report()["body_who"], flush=True)
if "abort" not in o_ and HOLD.holding(SD):
    print("ck", ck_save("n1_tissue_at_bin", kind="act", info=dict(note="tissue carried to the bin stance (AI-operated)")), flush=True)
    _bin_drop_lean(nm, SD)
    try:
        mon_start(target=None); MON["ignore_names"] = (tb_, bn_)
        crouch(0.0, 0.0, T=1.2); rest_hands(SIDES); op.run(0.5)
        tmove(fwd=-0.10, tag="off_bin")
    except Abort as ex_:
        print("off abort", ex_, flush=True)
    MON["on"] = False
print("tissue", np.round(centre(tb_), 3).tolist(), "inside", inside(tb_, bn_), "state", state(), "fell", fallen(), flush=True)
print("FIN", _finish(nm, "AI-operated night finisher: stance (-2.83,-0.51,124 deg), seat posture (-0.12,0.45), corner_pick right s_in 2.5 cm force 5 N (guard passed, rose 10 cm); put_away found no path -> carried by walk_tight to 0.40 m south of the bin, lean drop over its middle (2-stage servo), open"), flush=True)
print(look3("n1_tissue_bin"), flush=True)
