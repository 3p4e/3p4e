#!/usr/bin/env bash
# Downloads the OpenCV Zoo face models used by face_qc.py (not committed: 38 MB)
set -euo pipefail
cd "$(dirname "$0")" && mkdir -p models && cd models
base=https://huggingface.co/opencv
curl -sSLf -o face_detection_yunet_2023mar.onnx  $base/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx
curl -sSLf -o face_recognition_sface_2021dec.onnx $base/face_recognition_sface/resolve/main/face_recognition_sface_2021dec.onnx
pip install -q opencv-python-headless numpy
echo "models ready"
