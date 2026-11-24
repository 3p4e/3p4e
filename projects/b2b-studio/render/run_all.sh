#!/bin/bash
bash /workspace/setup_full.sh > /workspace/setup.log 2>&1
for b in 6 7 8 9 10 4 5; do
  [ -f /workspace/done_$b ] && continue
  rm -rf /workspace/v3bundle && mkdir -p /workspace/v3bundle && tar xzf /workspace/cb$b.tgz -C /workspace/v3bundle
  cp /workspace/batch_universal.py /workspace/v3bundle/batch.py
  cd /workspace && python3 /workspace/v3bundle/batch.py > /workspace/batch$b.log 2>&1 && touch /workspace/done_$b
done
echo ALL_DONE > /workspace/all_done
