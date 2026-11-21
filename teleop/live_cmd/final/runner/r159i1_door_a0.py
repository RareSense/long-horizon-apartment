ATTEMPT = 0
exec(open(r'E:\urc_final\scripts\home\final_run\common_a.py', encoding='utf-8').read())
exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
exec(open(r'E:\urc_final\scripts\home\final_run\items_lib.py', encoding='utf-8').read())
try:
    ZZ_OK = ITEM_FN['r159i1_door'](0)
except Exception:
    import traceback as _tbr
    print('ITEM_EXC', _tbr.format_exc()[-1500:], flush=True); ZZ_OK = False
print('ZZ_OK', ZZ_OK, flush=True)
