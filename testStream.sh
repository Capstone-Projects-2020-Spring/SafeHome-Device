gst-launch-1.0 videotestsrc pattern=ball \
    ! video/x-raw,width=480,height=640 \
    ! videoconvert \
    ! avenc_flv \
    ! flvmux \
    ! rtmpsink location='rtmp://localhost/thermal live=1'

