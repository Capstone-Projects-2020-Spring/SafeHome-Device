from gstreamer import GstContext, GstPipeline
import time

with GstContext():
    testPipeline = GstPipeline("videotestsrc pattern=zone-plate kx2=20 ky2=20 kt=1 \
    ! video/x-raw,width=480,height=640 \
    ! omxh264enc \
    ! h264parse \
    ! flvmux \
    ! rtmpsink location='rtmp://localhost/thermal live=1'")
    
    pipeline= GstPipeline("appsrc emit-signals=True is-live=True \
    caps=video/x-raw,format=RGB,width=640,height=480,framerate=30/1 \
    ! queue max-size-buffers=4 \
    ! omxh264enc \
    ! h264parse \
    ! flvmux \
    ! rtmpsink location='rtmp://localhost/thermal live=1'")
    
    appsrc = pipeline.get_by_cls(GstApp.AppSrc)[0]
    appsrc.set_property("format", Gst.Format.TIME)
    CAPS="video/x-raw,format=RGB,width=640,height=480,framerate=30/1"
    appsrc.set_caps(Gst.Caps.from_string(CAPS))
    appsrc.set_property("block", True)
    
    for _ in range(NUM_BUFFERS):  
     array = np.random.randint(low=0, high=255, \
                               size=(HEIGHT, WIDTH, CHANNELS),\
                               dtype=DTYPE)  
 

pipeline.startup()

time.sleep(100)

pipeline.shutdown()