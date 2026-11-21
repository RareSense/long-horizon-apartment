# the verification start: chain item 1071 (pouch) + its gotcha (posture 0 at once, 2 steps back tall), saved as kind "start"
# (kept by ck_prune_item, which deletes this item's act/roll checkpoints when an item ends ok)
MON["on"] = False
zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1120_093820_dex1_floor_12\checkpoints\1071_item_r149i1_pouch"); gait_on()
op.send(dict(cmd="posture", height=0.0, lean=0.0, duration=0.4)); op.run(1.2)
for k_ in range(2):
    tmove(fwd=-0.10, carry=("left",), tag="start_back")
sync_cloth(force=True); refresh_jointed_footprints(); rest_hands(SIDES)
op.run(4.0, until=_standing); op.run(1.5)
print("START", ck_save("scout_start", kind="start"), state(), "fell", fallen(), flush=True)
