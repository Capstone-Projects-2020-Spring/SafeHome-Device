gst-launch-1.0 videotestsrc \
    ! video/x-raw,width=480,height=640 \
    ! omxh264enc \
    ! h264parse \
    ! flvmux \
    ! rtmpsink location='rtmp://localhost/thermal live=1'

