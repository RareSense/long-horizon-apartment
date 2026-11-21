import sys, subprocess
sys.path.insert(0, r"E:\urc_final\scripts\home\final_run")
nm=sys.argv[1]; k=int(sys.argv[2])
FR=r"E:\urc_final\scripts\home\final_run"
code=(f"ATTEMPT = {k}\n"
      f"exec(open(r'{FR}\common_a.py', encoding='utf-8').read())\n"
      f"exec(open(r'{FR}\common_b.py', encoding='utf-8').read())\n"
      f"exec(open(r'{FR}\items_lib.py', encoding='utf-8').read())\n"
      f"try:\n    ZZ_OK = ITEM_FN['{nm}']({k})\nexcept Exception:\n    import traceback as _tbr\n"
      "    print('ITEM_EXC', _tbr.format_exc()[-1500:], flush=True); ZZ_OK = False\nprint('ZZ_OK', ZZ_OK, flush=True)\n")
p=rf"C:\Users\raresense\sim_home\apartment\live_cmd\final\fix1\{nm}_v{k}.py"
open(p,"w",encoding="utf-8").write(code)
r=subprocess.run(["py","-3.12",r"E:\urc_final\scripts\isaac_cmd.py","--port","47960",p],capture_output=True,text=True)
out="\n".join(l for l in (r.stdout+r.stderr).splitlines() if not l.startswith("Module ") and "UserWarning" not in l and "_convert_to_mjc" not in l and "warnings.warn" not in l)
open(p[:-3]+".out","w",encoding="utf-8").write(out)
print(out[-3000:])
