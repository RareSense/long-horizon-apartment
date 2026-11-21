ZZ_RELOAD = os.path.join(RUN, "checkpoints", "0167_item_r125i1_flat")
nm = "r175i1_cardboard_box"; b_ = body_of(nm); sp_ = DESC["spots"].get(nm) or [-5.14, 1.6]
print("spot", sp_, "box", np.round(centre(b_), 3).tolist(), "check", item_check(nm), flush=True)
if ZZ_RELOAD:
    ck_load(ZZ_RELOAD); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
    exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
    print("RELOADED", ZZ_RELOAD, "rec", rec.n, state(), "route", item_name(ROUTE[POS]), "done", len(DONE), flush=True)
_start_item(nm)
mon_start(target=None)
try:
    walk_tight((-4.87, 1.08, np.pi / 2))
except (Abort, RuntimeError) as ex_:
    print("walk ERR", str(ex_)[:200], flush=True)
MON["on"] = False
for stroke_ in range(3):
    if item_check(nm).get("ok") or fallen():
        break
    gap_ = float(obj_box(b_)[0][1]) - float(base()[0][1])
    if stroke_ > 0 and gap_ > 0.22:
        mon_start(target=None)
        try:
            tmove(fwd=float(min(0.12, gap_ - 0.20)), tag=f"box_closer{stroke_}")
        except Abort as ex_:
            print("closer abort", ex_, flush=True)
        MON["on"] = False
    try:
        r_ = push_floor(nm, (0.0, 1.0), (float(centre(b_)[0]), 0.0), float(sp_[1]), side="left", z=0.05)
        print("PUSH", stroke_, str(r_)[:400], "gap was", round(gap_, 3), flush=True)
    except Exception as ex_:
        print("push ERR", str(ex_)[:300], flush=True)
    MON["on"] = False
print("box", np.round(centre(b_), 3).tolist(), "check", item_check(nm), "state", state(), "fell", fallen(), flush=True)
if not fallen():
    try:
        crouch(0.0, 0.0, T=1.2); rest_hands(SIDES); op.run(1.0)
    except Exception:
        pass
    print("FIN", _finish(nm, "push_floor north along the wall in strokes (closed jaws, pad 5 cm), a short step closer between strokes (AI-operated night finisher)"), flush=True)
print(look3("n1_box_end"), flush=True)
