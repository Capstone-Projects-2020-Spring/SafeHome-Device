sudo /home/pi/mlx90640-library/examples/rawrgb 4 |  sudo gst-launch-1.0 fdsrc  blocksize=2304  \
 ! rawvideoparse framerate=4/1 width=32 height=24  use-sink-caps=false \
 ! videoscale method=0  ! video/x-raw,width=640,height=480,framerate=4/1 \
 ! omxh264enc\
 ! h264parse\
 ! flvmux\
! rtmpsink location= 'rtmp://localhost/thermal live=1'
# ! filesink="testvideo.flv" -e
# ! flvmux \
# ! fakesink
# ! videorate\


#sudo mlx90640-library/examples/rawrgb 8 | sudo gst-launch-1.0 -v fdsrc\
# blocksize=2304 ! queue \
# ! rawvideoparse  use-sink-caps=true width=32 height=24 framerate =16/1 format=rgb\
# ! avenc_h264_omx\
# ! fakesink

#! h264parse \
#! flvmux \
#! filesink location="rec_thermal.flv" -e
#! rtmpsink location='rtmp://localhost/thermal live=1'
#gst-launch-1.0  videotestsrc ! tee \
#! video/x-raw,width=480,height=640 \
#! avenc_h264_omx \
#! h264parse ! flvmux ! rtmpsink location='rtmp://localhost/thermal live=1'
#! v4l2h264enc \

#gst-launch-1.0 v4l2src device=/dev/i2c-1 ! filesink="wagabagaboo" -e

#gst-launch-1.0 rpicamsrc bitrate=250000 rotation=270  annotation-mode=date+time\
# ! video/x-h264,width=480,height=640,framerate=30/1,profile=high\
# ! h264parse !  flvmux ! rtmpsink location='rtmp://localhost/live live=1'

