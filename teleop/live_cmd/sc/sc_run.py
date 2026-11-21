# run FILE_ in the session; on an error print only a short traceback (AI-operated, scout)
import traceback as _tb
try:
    exec(open(FILE_, encoding="utf-8-sig").read())
except Exception as _ex:
    _s = _tb.format_exc().splitlines()
    print("ERROR", "\n".join(l_[:300] for l_ in _s[-8:]))
