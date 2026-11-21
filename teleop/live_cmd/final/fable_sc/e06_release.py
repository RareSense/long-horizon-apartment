# AI-operated (Fable escalation, scooter r126): the scooter stands on its rear wheel and a front wheel, the jaws hold the
# bar with 6 N only. Checkpoint, then the skill's release: jaws open, hands straight back off the bar, to rest.
print("ck", ck_save("fsc_standing_before_release", kind="act", info=dict(note="scooter stands by the sofa arm, jaws still round the bar at 6 N (AI-operated)")), flush=True)
mon_start(target=sc_); MON["t_max"] = 6000.0
try:
    r_ = sh_release(sc_)
    print("RELEASE", r_, flush=True)
except Abort as ex_:
    print("ABORT", str(ex_)[:400], flush=True)
MON["on"] = False
st_ = sh_state(sc_); lo_, hi_ = obj_box(sc_)
print("after: tilt", st_["tilt"], "bar", st_["bar"], "floor", sh_on_floor(sc_), "touch", st_["touch"], "box", np.round(lo_, 3).tolist(), np.round(hi_, 3).tolist(), "centre", np.round(centre(sc_), 3).tolist(),
      "contacts", contact_report(), "state", state(), "fallen", fallen(), "rec", rec.n, flush=True)
bid_ = m.body(sc_).id; md_ = br.mjd; who_ = {}
for i_ in range(int(md_.ncon)):
    c_ = md_.contact
    if c_.dist[i_] > 0.001:
        continue
    g0_, g1_ = int(c_.geom[i_][0]), int(c_.geom[i_][1])
    b0_, b1_ = int(br.sb_of_ib[br.geom_body[g0_]]), int(br.sb_of_ib[br.geom_body[g1_]])
    if bid_ in (b0_, b1_):
        o_ = b1_ if b0_ == bid_ else b0_; gs_ = g0_ if b0_ == bid_ else g1_
        who_[(gs_, m.body(o_).name)] = who_.get((gs_, m.body(o_).name), 0) + 1
print("scooter contacts (its geom, other body)", who_, flush=True)
views("e06")
pth_ = os.path.join(TELE_DIR, "fsc_e06_east.jpg"); close(pth_, np.array([-1.0, -0.6, 1.3]), np.array([-2.2, -0.05, 0.4]), "AI-operated | scooter from the south-east")
pth2_ = os.path.join(TELE_DIR, "fsc_e06_south.jpg"); close(pth2_, np.array([-2.05, -1.5, 1.1]), np.array([-2.2, -0.05, 0.4]), "AI-operated | scooter from the south")
print("VIEWS2", pth_, pth2_, flush=True)
