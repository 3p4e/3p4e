f=/workspace/send_wan22_test_832x480_00001_.mp4
echo "C2META 480 $(stat -c%s $f) $(sha256sum $f | cut -d' ' -f1)"
base64 -w 380 $f | awk '{print "C2 480 " NR " " $0}'
