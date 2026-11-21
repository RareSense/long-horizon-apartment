# Sponges r83i1 -> tray table r94 south strip (Fable's call, AI-operated), with the two-hand squeeze guard (c00).
MON["on"] = False
exec(open(r"E:\urc_fable3\scripts\home\kitchen_skills.py", encoding="utf-8").read())
exec(open(r"E:\urc_fable3\scripts\home\island_skills.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\f14\c00_sponge_guard.py", encoding="utf-8").read())
zz_b = SPONGE
zz_t = body_of("r94i1_tray_table")
# preconditions: dishwasher shut, nothing on the tray's south strip (x 1.40-1.69, y 1.48-1.60, above the top 0.755)
dwq_ = {}
for n_ in dw_names():
    try:
        j_ = [jj for jj in range(m.njnt) if int(m.jnt_bodyid[jj]) == m.body(n_).id]
        if j_:
            dwq_[n_] = round(float(d.qpos[m.jnt_qposadr[j_[0]]]), 3)
    except Exception:
        pass
strip_ = []
for b_ in INFO["bodies"]:
    if b_ in (zz_b, zz_t):
        continue
    lo_, hi_ = obj_box(b_)
    if hi_[0] > 1.40 and lo_[0] < 1.69 and hi_[1] > 1.48 and lo_[1] < 1.60 and hi_[2] > 0.75 and lo_[2] < 1.0:
        strip_.append(b_)
print("dishwasher joints", dwq_, "tray strip things", strip_, "sponge", np.round(obj_box(zz_b)[0], 3).tolist(), np.round(obj_box(zz_b)[1], 3).tolist(), flush=True)
print("robot", state(), "held", HELD, "kit", kit_mem(), flush=True)
if not strip_:
    zz_r = call_mon(lambda: island_pick(zz_b, stand=globals().get("SP_STAND", (0.708, 0.066, 0.0)), put_stand=(1.54, 1.25, 90.0), spot=(1.545, 1.535), z_top=0.7553, roll=True),
                    "r83i1_sponges", target=zz_b, ignore_names=(zz_t,), ck=False)
    print("RESULT", {k: v for k, v in zz_r.items() if k != "record"}, flush=True)
    print("RECORD", str({k: v for k, v in (zz_r.get("record") or {}).items() if k in ("ok", "error", "roll", "walk", "sim_s", "wall_s")})[:1500], flush=True)
    print("PICKS", str((zz_r.get("record") or {}).get("picks"))[:900], flush=True)
    print("PUTS", str((zz_r.get("record") or {}).get("puts"))[:900], flush=True)
    print("SQUEEZE CHECKS", SPONGE_CHECK, flush=True)
print("sponge now", np.round(obj_box(zz_b)[0], 3).tolist(), np.round(obj_box(zz_b)[1], 3).tolist(), "touching", _thing_contacts(zz_b), state(), "fell", fallen(), "kit", kit_mem(), flush=True)
