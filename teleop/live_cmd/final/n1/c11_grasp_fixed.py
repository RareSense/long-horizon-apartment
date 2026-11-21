ck_load(r"C:\Users\raresense\sim_home\runs\1121_021343_dex1_floor_final_s2\checkpoints\0231_act_n1_stock_near"); gait_on(); settle_after_load(); refresh_jointed_footprints(); rest_hands(SIDES); op.run(1.0)
print("RELOADED 0231 rec", rec.n, flush=True)
zz_n = "r190i1_stocking"; zz_cb = body_of("r186i1_basket")
_sf0 = stance_for
def stance_for(pt, sd, *a, **k):
    yw_ = -np.pi / 2
    if sd != "right" or np.linalg.norm(np.asarray(pt[:2]) - np.array([-2.85, -1.75])) > 0.08:
        return (None, np.inf) if k.get("with_cost") else None
    g_ = np.asarray(pt[:2], float) - RM.rz(yw_)[:2, :2] @ np.array([X_REL, -Y_REL])
    return ((float(g_[0]), float(g_[1]), yw_), 0.0) if k.get("with_cost") else (float(g_[0]), float(g_[1]), yw_)
mon_start(target=None); MON["t_max"] = 900.0; MON["ignore_names"] = (zz_cb,)
zz_o = dict()
try:
    zz_pk = with_tight(lambda: grasp_cloth(zz_n, "right"))
    zz_o["pick"] = dict(ok=zz_pk.get("ok"), side=zz_pk.get("side"), tries=[str(t_)[:200] for t_ in zz_pk.get("tries", [])], err=zz_pk.get("error"))
except Abort as ex_:
    zz_o["abort"] = str(ex_)
except RuntimeError as ex_:
    zz_o["error"] = str(ex_)[:300]
finally:
    stance_for = _sf0
MON["on"] = False
print("PICK", zz_o, "state", state(), "fell", fallen(), "touch", contact_report()["body_who"], "held", list(HELD), list(LOCK) if "LOCK" in globals() else None, flush=True)
print("look", look3("n1_stock_pick_fixed"), flush=True)
