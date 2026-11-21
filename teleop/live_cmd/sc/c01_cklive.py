# live apply (coordinator 20 Nov): ck_prune_item keeps act meta.json; PRE_ACTION appends to RUN\actions.jsonl (home-cleaning 5b7002f)
import json as _json
_src = open(r"C:\Users\raresense\sim_home\apartment\live_cmd\sc\_ck_new.py", encoding="utf-8").read()
_i = _src.index("def ck_prune_item("); _j = _src.index("def ck_disk(")
exec(_src[_i:_j])
_i = _src.index("def _action_log("); _j = _src.index("def _short(")
exec(_src[_i:_j])
print("ck live patch: ck_prune_item keeps meta.json, PRE_ACTION -> actions.jsonl", os.path.join(RUN, "actions.jsonl"), flush=True)
