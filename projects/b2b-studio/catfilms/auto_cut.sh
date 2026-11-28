#!/bin/bash
# one pass: pull finished category clips from both boxes (checksummed), cut every film whose clips, VO and music are all there
S=/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad; R=/home/user/3p4e/projects/b2b-studio/catfilms; cd $S; mkdir -p catfilms/clips
for round in 1; do   # one pass per call (a monitor re-runs it)
  for b in A B; do
    L=$(timeout 90 python3 rsh.py "timeout 60 /opt/abra-v3/fv$b.sh 'ls /workspace/cfout'" 80 2>/dev/null | grep "^cf_.*mp4$" | while read f; do [ -f catfilms/clips/$f ] || echo /workspace/cfout/$f; done | paste -sd,)
    [ -n "$L" ] && timeout 1500 python3 fv2/fpull.py $b "$L" catfilms/clips 2>&1 | grep -c "^got" | sed "s/^/pulled $b: /"
  done
  /usr/bin/python3 $R/cut.py catfilms/clips catfilms/cuts 2>&1 | grep -E "^OK|CUT_DONE|Error|Traceback"
  [ $(ls catfilms/cuts/cf_*.mp4 2>/dev/null | wc -l) -ge 56 ] && echo ALL_CUT && break

done
