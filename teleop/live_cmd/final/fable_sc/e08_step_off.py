# AI-operated (Fable escalation, scooter r126): the scooter stands, hands at rest. Step away: the rear wheel stands 3 cm
# beside / 7 cm behind the right heel (seen from above), so SIDEWAYS (east) first, twice, then two steps back.
TELE_V, TELE_W, CARRY_LOW = FSC_OLD
print("ck", ck_save("fsc_released", kind="act", info=dict(note="scooter parked standing by the sofa's east arm, hands at rest, robot beside it (AI-operated)")), flush=True)
mon_start(); MON["t_max"] = 600.0
box0_ = [np.round(v_, 3).tolist() for v_ in obj_box(sc_)]
try:
    for kw_ in (dict(side=0.15), dict(side=0.15), dict(fwd=-0.15), dict(fwd=-0.15)):
        r_ = tmove(tag="fsc_off", **kw_)
        print("off", kw_, "->", r_["at"], r_["yaw_deg"], r_["touch"], "fell", r_["fell"], "why", MON.get("why"), flush=True)
        if MON.get("why") or r_["fell"]:
            break
except Abort as ex_:
    print("ABORT", str(ex_)[:300], flush=True)
MON["on"] = False
st_ = sh_state(sc_)
print("scooter: tilt", st_["tilt"], "bar", st_["bar"], "floor", sh_on_floor(sc_), "box before", box0_, "now", [np.round(v_, 3).tolist() for v_ in obj_box(sc_)], "centre", np.round(centre(sc_), 3).tolist(), flush=True)
print("robot", state(), "fallen", fallen(), "held", _held_any(), "rec", rec.n, flush=True)
print("LOOK", look3("fsc_e08_off"), flush=True)
pth_ = os.path.join(TELE_DIR, "fsc_e08_east.jpg"); close(pth_, np.array([-0.9, -0.9, 1.4]), np.array([-2.1, 0.0, 0.45]), "AI-operated | scooter parked, from the south-east")
print("VIEW", pth_, flush=True)
