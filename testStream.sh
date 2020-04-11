gst-launch-1.0 appsrc emit-signals=True is-live=True \
    ! video/x-raw,width=480,height=640 \
    ! videoconvert \
    ! avenc_flv \
    ! flvmux \
    ! rtmpsink location='rtmp://localhost/thermal live=1'

