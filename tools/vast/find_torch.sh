#!/bin/bash
set -uo pipefail
for cu in cu126 cu128; do
  echo "=== $cu torch (cp311 linux x86_64, distinct) ==="
  curl -s "https://download.pytorch.org/whl/$cu/torch/" \
    | grep -oE "torch-[0-9]+\.[0-9]+\.[0-9]+(%2B|\+)${cu}-cp311-cp311-linux_x86_64\.whl" \
    | sed 's/%2B/+/g' | sort -uV | tail -10
  echo "=== $cu torchvision ==="
  curl -s "https://download.pytorch.org/whl/$cu/torchvision/" \
    | grep -oE "torchvision-[0-9]+\.[0-9]+\.[0-9]+(%2B|\+)${cu}-cp311-cp311-linux_x86_64\.whl" \
    | sed 's/%2B/+/g' | sort -uV | tail -4
  echo
  echo "=== $cu torchaudio ==="
  curl -s "https://download.pytorch.org/whl/$cu/torchaudio/" \
    | grep -oE "torchaudio-[0-9]+\.[0-9]+\.[0-9]+(%2B|\+)${cu}-cp311-cp311-linux_x86_64\.whl" \
    | sed 's/%2B/+/g' | sort -uV | tail -4
  echo
  echo "=== distinct torch MINOR lines on $cu (to see if 2.13 exists) ==="
  curl -s "https://download.pytorch.org/whl/$cu/torch/" \
    | grep -oE "torch-[0-9]+\.[0-9]+\.[0-9]+(%2B|\+)${cu}" | sed 's/%2B/+/g' | sort -uV | tail -6
  echo "----"
done
echo "=== LTX-2 pyproject dependencies block ==="
sed -n '/dependencies = \[/,/^\]/p' /workspace/LTX-2/pyproject.toml 2>/dev/null | head -60
