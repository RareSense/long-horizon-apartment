ZZ = tele_item_done("r195i3_paper", note="go_item pick (guarded) + carry; monitor stop (left knee on the bin 25 N); AI teleop: step back 0.08, squat -0.15 lean 0.6, hand over the bin middle, open (AI-operated)")
print("DONE", ZZ, flush=True)
# StateRec check: recorded particles at the episode start vs the true particle state now (garments not yet touched)
import urc.tasks.home.staterec as _SRC
rec.srec.flush()
L_, it_ = _SRC.load_states(os.path.join(RUN, "states"), frames=(100, 1801))
got_ = {}
for fr_, k_, t_, q_s, cam_, cl_ in it_:
    if fr_ in (100, 1799, 1800, 1801):
        got_[fr_] = cl_
for g_, G_ in GARMENTS.items():
    P_ = np.asarray(G_["w"].points(0))
    print("garment", g_, {fr_: (None if c_.get(g_) is None else round(float(np.abs(np.asarray(c_[g_]) - P_).max()), 4)) for fr_, c_ in got_.items()}, flush=True)
# cloth visuals: the loader missed sync_cloth(force=True) after the start load (stale garment drawing until a sync)
try:
    print("sync_cloth", sync_cloth(force=True), flush=True)
except Exception as ex_:
    print("sync_cloth ERR", str(ex_)[:200], flush=True)
print("SAY", say_item(), flush=True)
