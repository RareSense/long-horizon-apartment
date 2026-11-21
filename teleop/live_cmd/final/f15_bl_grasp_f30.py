# blanket grasp the way Fable did it (fb\b01-b04, AI-operated): particle 136 (uv -0.43,0), right hand, stance with the
# blanket's own rectangle kept clear (Fable's: (0.91,-1.50,30 deg)), crouch over, jaws 1.5 mm into the cloth, close, lift, stand.


zz_ip = 136; zz_sd = "right"
if fallen() or float(base()[0][2]) < 0.6:
    stand_up()
print("goal", np.round(zz_goal, 3).tolist(), flush=True)
rest_hands((zz_sd,), T=0.3)
zz_wk = zz_walk_stance(zz_goal)
print("walk", {k_: (v_ if not isinstance(v_, (list, dict)) or k_ in ("goal", "base", "abort") else str(v_)[:160]) for k_, v_ in (zz_wk or {}).items()}, flush=True)
print(state(), contact_report(), "in_reach", in_reach(zz_w().points(0)[zz_ip], zz_sd), flush=True)
zz_r = zz_crouch_over(zz_ip, zz_sd); zz_Q = zz_r.pop("Q")
print("crouch_over", zz_r, flush=True)
print("down", zz_jaws_down(zz_sd, zz_Q), flush=True)
zz_c = zz_close_lock(zz_sd)
print("close_lock", zz_c, flush=True)
if zz_c["caught"]:
    zz_z0 = float(garment_box(zz_BL)[1][2])
    PRE_ACTION("zz_lift", dict(side=zz_sd))
    zz_hp = ts.ee_pose(zz_sd)[0]
    op.move({zz_sd: [zz_hp[0], zz_hp[1], zz_hp[2] + 0.08]}, speed=0.06, quats=zz_Q, timeout=4.0, tol=0.008); op.run(0.4)
    print("rose", round(float(garment_box(zz_BL)[1][2]) - zz_z0, 3), "held uv", np.round(zz_uv()[LOCK[zz_sd][1]].mean(0), 3).tolist(), flush=True)
    stand_with(zz_sd); op.run(1.0)
    print("stood", zz_stat(), "hang", zz_hang(zz_sd), "cloth_held", cloth_held(zz_sd), flush=True)
else:
    open_jaws(zz_sd, T=0.3); rest_hands((zz_sd,)); stand_up()
print("look", look3("bl_grasp_f30"), flush=True)
