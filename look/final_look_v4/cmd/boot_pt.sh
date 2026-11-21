# AI-operated: fresh Isaac (slot cloth, 47970) -> episode START state (s00_start.py, no checkpoint) -> PT stills (p10_pt.py).
# Args: python snippet with SHOTS_/OUTD_/SPP_/ISO_/VIEWS_ globals. Leaves Isaac running (stop with c_live.py stop 47970).
set -u
D=/c/Users/raresense/sim_home/apartment/final_look_v4/cmd
cd /e/urc_look
export URC_TEXTURED=1 URC_ROUGH_FLOOR=0.8 URC_NEWTON_CPU=1 URC_QP_SOLVER=daqp
py -3.12 scripts/home/c_live.py stop 47970 >/dev/null 2>&1
rm -rf /c/Users/raresense/sim_home/_cloth/_pyc_live/*
py -3.12 scripts/home/c_live.py start 47970 2>&1 | tail -1
(py -3.12 "$D/guard.py" &)
py -3.12 scripts/isaac_cmd.py --port 47970 "$D/s00_start.py" 2>&1 | grep "props:\|START_LOADED\|Traceback\|Error" | cut -c1-500
py -3.12 scripts/isaac_cmd.py --port 47970 -c "
$1
exec(open(r'$(cygpath -w $D)\p10_pt.py',encoding='utf-8').read())" 2>&1 | grep "pt_1080\|TIMES\|ERR\|Traceback\|Error" | cut -c1-400
