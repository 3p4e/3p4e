f=/workspace/send_wan22_test_1280x720_00001_.mp4
base64 -w 380 $f | awk 'NR>800 {print "C2 720 " NR " " $0}'
