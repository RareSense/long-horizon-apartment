#!/bin/bash
# wait.sh <name> [lines]: wait up to ~165 s for <name>.out to end (__END__), then show its tail
D=/c/Users/raresense/sim_home/apartment/live_cmd/final
for i in $(seq 1 33); do grep -q "__END__" $D/$1.out 2>/dev/null && break; sleep 5; done
grep -q "__END__" $D/$1.out 2>/dev/null || echo "(still running)"
grep -v "Module \|UserWarning\|_convert_to_mjc\|warnings.warn\|precompute" $D/$1.out 2>/dev/null | tail -${2:-14}
