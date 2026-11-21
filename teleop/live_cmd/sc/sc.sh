#!/bin/bash
# sc.sh <file.py> ["python prefix;"]  run a command file in the SCOUT (hall) cloth-slot Isaac, port 47970 (AI-operated)
D='C:/Users/raresense/sim_home/apartment/live_cmd/sc'
code="${2}FILE_=r'$D/$1'; exec(open(r'$D/sc_run.py').read())"
py -3.12 'E:/urc_scout/scripts/isaac_cmd.py' --port 47970 -c "$code" 2>&1 | grep -v 'checkpoint\] saved\|^Module \|UserWarning\|_convert_to_mjc\|Warning' | cut -c1-${SC_CUT:-3000} | tee "$D/${1%.py}.out"
