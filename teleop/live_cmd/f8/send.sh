#!/bin/bash
# send a session command file and print its filtered output
cd /e/urc_home && py -3.12 scripts/isaac_cmd.py --port 47960 "C:/Users/raresense/sim_home/apartment/live_cmd/f8/$1" 2>&1 | grep -v "Warning\|^Module \|UserWarning\|_convert_to_mjc" | tail -${2:-40}
