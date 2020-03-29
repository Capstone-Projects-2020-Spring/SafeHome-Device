#!/bin/bash

gst-launch-1.0 rpicamsrc bitrate=250000 rotation=270  annotation-mode=date+time\
 ! video/x-h264,width=480,height=640,framerate=30/1,profile=high\
 ! h264parse !  flvmux ! rtmpsink location='rtmp://localhost/live live=1'
#| gst-launch-1.0 rpicamsrc bitrate=250000 rotation=0 annotation-mode=date+time\
# ! video/x-h264,width=480,height=640,framerate=30/1\
# ! h264parse ! flvmux ! rtmpsink location='rtmp://localhost/low live=1'\
#| gst-launch-1.0 rpicamsrc bitrate=250000  rotation=0 annotation-mode=date+time\
# ! video/x-h264,width=720,height=1280,framerate=30/1\
# ! h264parse ! flvmux ! rtmpsink location ='rtmp://localhost/mid live=1'\
#| gst-launch-1.0 rpicamsrc bitrate=250000  rotation=0 annotation-mode=date+time\
# ! video/x-h264,width=1080,height=1920,framerate=30/1\
# ! h264parse ! flvmux ! rtmpsink location ='rtmp://localhost/high live=1'



#gst-launch-1.0 rpicamsrc bitrate=250000 rotation=180 ! video/x-h264,width=640,height=360,framerate=15/1,profile=high ! h264parse ! flvmux ! rtmpsink location='rtmp://localhost/live live=1'

