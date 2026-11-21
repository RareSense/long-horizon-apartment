MON["on"] = False
CK = r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\0864_act_sh_set_down_leg"
zz_m = route_v3_resume(CK)
gait_on()
SB = body_of("r126i1_scooter"); SC_NAME = "r126i1_scooter"
globals()["TELE_V"] = V_CARRY_HEAVY; globals()["TELE_W"] = 0.10; globals()["CARRY_LOW"] = False
print("ext", [k_ for k_ in ts.ctrl.ext], "ee modes", {s_: (ts.ee.get(s_) or {}).get("mode") for s_ in SIDES}, flush=True)


def sc_report(tag):
    st_ = sh_state(SB); w_ = sh_wheel(SB)
    r_ = dict(seat=sh_seat(SB), touch={s_: sum(finger_touch(s_, SB).values()) for s_ in SIDES}, tilt=st_["tilt"], wheel_x=round(w_["x"], 3), x_up=round(w_["x_up"], 3),
              bar_z=round(w_["bar_z"], 3), arc=round(w_["arc"](max(w_["x"], 0.0)) + float(np.clip(w_["z"] - w_["r"], 0, 0.03)), 3), on_floor=len(sh_on_floor(SB)), pelvis=state()["pelvis"], fell=fallen())
    print(tag, r_, flush=True)
    for s_ in SIDES:
        pm_ = pad_mid(s_); sg_ = 1.0 if s_ == "left" else -1.0
        p_, y_ = base(); lat_ = RM.rz(y_)[:2, 1]
        close(os.path.join(TELE_DIR, f"f12_{tag}_{s_}.jpg"), np.r_[pm_[:2] + lat_ * sg_ * 0.30, pm_[2] + 0.10], pm_, f"{tag} {s_} jaw")
    return r_


# hold the bar steady (zero-velocity hand commands) while the load settles
op.run(1.0, [dict(cmd="ee", name=s_, mode="velocity", linear=[0, 0, 0], frame="world", ttl=0.3) for s_ in SIDES])
R0 = sc_report("t01")
