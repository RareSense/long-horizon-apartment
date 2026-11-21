# AI-operated (Fable escalation, scooter r126): released. Pictures and what the scooter touches (no motion).
st_ = sh_state(sc_); F_ = sh_frame(sc_)
print("tilt", st_["tilt"], "bar", st_["bar"], "deck_deg", st_["deck_deg"], "floor pieces", sh_on_floor(sc_), "centre", np.round(centre(sc_), 3).tolist(), "state", state(), flush=True)
bid_ = m.body(sc_).id; md_ = br.mjd; who_ = {}
try:
    for i_ in range(int(md_.ncon)):
        c_ = md_.contact
        if c_.dist[i_] > 0.001:
            continue
        g0_, g1_ = int(c_.geom[i_][0]), int(c_.geom[i_][1])
        if g0_ < 0 or g1_ < 0:
            continue
        b0_, b1_ = int(br.sb_of_ib[br.geom_body[g0_]]), int(br.sb_of_ib[br.geom_body[g1_]])
        if bid_ in (b0_, b1_):
            o_ = b1_ if b0_ == bid_ else b0_; gs_ = g0_ if b0_ == bid_ else g1_
            nm_ = m.body(o_).name if 0 <= o_ < m.nbody else str(o_)
            who_[(gs_, nm_)] = who_.get((gs_, nm_), 0) + 1
    print("scooter contacts (its geom, other body)", who_, flush=True)
except Exception as ex_:
    print("contacts:", str(ex_)[:200], flush=True)
print("LOOK", look3("fsc_e07_released"), flush=True)
for k_, (e_, lab_) in enumerate([(np.array([-1.0, -0.7, 1.3]), "from the south-east"), (np.array([-2.1, -1.6, 1.1]), "from the south"), (np.array([-2.15, -0.02, 2.38]), "from above (north up)")]):
    pth_ = os.path.join(TELE_DIR, f"fsc_e07_v{k_}.jpg"); close(pth_, e_, np.array([-2.15, -0.05, 0.4 if k_ < 2 else 0.0]), "AI-operated | scooter " + lab_)
    print("VIEW", pth_, flush=True)
