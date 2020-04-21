from gstreamer import GstContext, GstPipeline
import time

with GstContext():
    pipeline = GstPipeline("videotestsrc pattern=zone-plate kx2=20 ky2=20 kt=1 \
    ! video/x-raw,width=480,height=640 \
    ! omxh264enc \
    ! h264parse \
    ! flvmux \
    ! rtmpsink location='rtmp://localhost/thermal live=1'")
 

pipeline.startup()

time.sleep(100)

pipeline.shutdown()