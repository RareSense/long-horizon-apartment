ck_load(os.path.join(RUN, "checkpoints", "3140_item_r158i1_tissue")); gait_on()
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.3)); op.run(0.4)
refresh_jointed_footprints()
print("RELOADED 3140 rec", rec.n, state(), "touch", contact_report()["body_who"], flush=True)
MON["on"] = False
for k_ in range(2):
    try:
        r_ = tmove(fwd=-0.10, carry=("right",), tag="off_bin_tall")
        print("back", r_["at"], r_["touch"], flush=True)
    except Abort as ex_:
        print("abort", ex_, flush=True)
rest_hands(SIDES); op.run(1.0)
print("state", state(), "fell", fallen(), "touch", contact_report()["body_who"], flush=True)
if not fallen() and contact_report()["body"] < 1.0:
    print("ck", ck_save("n1_off_bin", kind="act", info=dict(note="two tall steps back off the bin after the tissue (AI-operated)")), flush=True)
