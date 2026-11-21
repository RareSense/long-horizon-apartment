CHAIN = r"C:\Users\raresense\sim_home\runs\1120_004212_dex1_floor_6\checkpoints\0379_item_r121i1_jacket"
exec(open(r"E:\urc_home\scripts\home\live\load_floor.py", encoding="utf-8").read())
exec(open(r"C:\Users\raresense\sim_home\apartment\live_cmd\fb\zz_help.py", encoding="utf-8").read())
print("RUN", RUN, "SEG", SEG.get("from_ckpt"), flush=True)
print("route head", [item_name(s_) for s_ in ROUTE[POS:POS + 4]], "done", DONE, flush=True)
print(zz_stat(), flush=True)
