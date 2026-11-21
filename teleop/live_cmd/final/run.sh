#!/bin/bash
# run.sh <name> [lines]: send <name>.py to the session; output to <name>.out, "__END__" appended when it returns
D=/c/Users/raresense/sim_home/apartment/live_cmd/final
cd /e/urc_final && py -3.12 scripts/isaac_cmd.py --port 47960 $D/$1.py > $D/$1.out 2>&1
echo "__END__" >> $D/$1.out
grep -v "Module \|UserWarning\|_convert_to_mjc\|warnings.warn\|precompute" $D/$1.out | tail -${2:-30}
