A_, ax_, a_, bid_, j_ = hinge_axis("r159i1_door")
qd_ = float(d.qpos[a_])
print("door q", round(qd_, 3), "shut range end", np.round(m.jnt_range[j_], 3).tolist(), "off deg", round(abs(np.degrees(qd_ - float(m.jnt_range[j_][0]))), 2), flush=True)
lo_, hi_ = body_aabb(bid_)
eye_ = np.r_[(lo_[:2] + hi_[:2]) / 2, 0.0] + np.array([0.0, 1.1, 0.9]); at_ = np.r_[(lo_[:2] + hi_[:2]) / 2, 0.3]
print(close(os.path.join(RUN, "look", "f14_b02_door_shut.jpg"), eye_, at_, f"TV door r159 q {qd_:.3f} (shut -1.571) (AI-operated)"), flush=True)
if abs(np.degrees(qd_ - float(m.jnt_range[j_][0]))) < 3.0:
    print("DONE", item_done_auto("r159i1_door", dict(status="done", q=round(qd_, 3), how="kitchen_skills.close_door_follow x2 (8 stages) under call_mon, f14\\b01_door.py (AI-operated)")), flush=True)
print("state", state(), "kit", kit_mem(), flush=True)
