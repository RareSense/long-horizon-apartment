ROOM = r'E:\urc_final\rooms\apartment_1122_full.json'; RUN = r'C:\Users\raresense\sim_home\runs\1120_181556_dex1_floor_final'; TASK = []; LIVE = True
exec(open(r'E:\urc_final\scripts\home\episode.py', encoding='utf-8').read())
print('CPU', CPU, type(br).__name__, state())
print('FINAL_LOOK', globals().get('FINAL_LOOK'), 'rec', type(globals().get('rec')).__name__, flush=True)
