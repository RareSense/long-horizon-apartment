zz_m = route_v3_resume(r"C:\Users\raresense\sim_home\runs\1119_211852_dex1_floor_3\checkpoints\0111_item_aside_r193i1_toy_piece")
TUCK_JOINTS = False
STANCE_LOW_ROOM = 0.35
STANCE_FUR_ROOM = 0.32
exec(open(r"E:\urc_home\scripts\home\live\scooter.py", encoding="utf-8").read())
print(state())
zz_r = park_scooter_sofa()
print("SCOOTER", {k_: v_ for k_, v_ in zz_r.items() if k_ not in ("look", "moves")})
print("moves", zz_r.get("moves"))
print("look", zz_r.get("look"), "mem", kit_mem())
