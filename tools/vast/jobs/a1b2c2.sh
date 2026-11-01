f=/workspace/send_wan22_test_1280x720_00001_.mp4
echo "C2META 720 $(stat -c%s $f) $(sha256sum $f | cut -d' ' -f1)"
base64 -w 380 $f | awk 'NR<=800 {print "C2 720 " NR " " $0}'
