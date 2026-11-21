ATTEMPT = 1
exec(open(r'E:\urc_final\scripts\home\final_run\common_a.py', encoding='utf-8').read())
exec(open(r'E:\urc_final\scripts\home\final_run\common_b.py', encoding='utf-8').read())
exec(open(r'E:\urc_final\scripts\home\final_run\items_lib.py', encoding='utf-8').read())
try:
    ZZ_OK = ITEM_FN['r190i1_stocking'](1)
except Exception:
    import traceback as _tbr
    print('ITEM_EXC', _tbr.format_exc()[-1500:], flush=True); ZZ_OK = False
print('ZZ_OK', ZZ_OK, flush=True)
