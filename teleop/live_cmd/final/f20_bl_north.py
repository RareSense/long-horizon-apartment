# blanket, AI teleop fix: Fable's FRONT stance NORTH of the hamper facing south (the west stance left the strand out of
# the left hand's reach). Reload 0800 (blanket held right at the entry), carry with the heading fixed, then the stages.
zz_n = "r117i1_blanket"; zz_h = laundry_body()
CK_RELOAD = os.path.join(CK_DIR, "0800_act_bc_blanket_held_right")
ck_load(CK_RELOAD); gait_on(); op.run(0.3)
try:
    sync_cloth(force=True)
except Exception as ex_:
    print("sync", ex_)
print("RELOADED", CK_RELOAD, "frame", rec.n, state(), "LOCK", list(LOCK), "held", cloth_held("right"), flush=True)
BC_YAW_ONLY = -np.pi / 2


def bc_front(name, cont):
    c_, r_ = bc_wall(cont); p_, _ = base()
    best_ = None

    def scan():
        nonlocal best_
        g_ = room_grid((name,)); g2_ = room_grid((name, cont))
        for yw_ in [BC_YAW_ONLY]:
            u_ = np.array([np.cos(yw_), np.sin(yw_)])
            pre_ = c_ - u_ * (r_ + BC_PRE_GAP); st_ = c_ - u_ * (r_ + BC_WALL_GAP)
            fr_ = g_.free(pre_, -0.03); fr2_ = [g2_.free(c_ - u_ * (r_ + gp_), -0.07) for gp_ in (BC_WALL_GAP, 0.35, 0.42)]
            dist_ = g_.reach_cost(p_[:2], pre_)
            print("[bc_front fixed]", np.round(pre_, 3).tolist(), "free", fr_, fr2_, "cost", round(float(dist_), 2), flush=True)
            if np.isfinite(dist_):
                best_ = (dist_, (float(pre_[0]), float(pre_[1]), float(wrapa(yw_))), (float(st_[0]), float(st_[1])))
    with_tight(scan)
    if best_ is None:
        raise RuntimeError(f"no front stance at {cont}")
    return best_[1], best_[2]


BC["stage"] = "grasp"
zz_r = bigcloth_into(zz_n, s1="right", start="carry", stop_after=globals().get("BL_STOP", "strand"))
for r_ in zz_r:
    print("RESULT", {k_: (v_ if not isinstance(v_, (dict, list)) else str(v_)[:220]) for k_, v_ in r_.items() if k_ != "look"}, flush=True)
print("held L/R", cloth_held("left"), cloth_held("right"), "inside", in_container(zz_n, zz_h), "state", state(), "touch", contact_report(), "fell", fallen(), flush=True)
print("look3", look3("bl_north"), flush=True)
