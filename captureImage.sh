#!/bin/bash

filename=$(date -u +"%Y%m%d_%H:%M:%S")_%04d.jpg
raspistill -o /home/pi/FTP/files/$filename -tl 1000 -t 7200000 > /home/pi/camera.log 2>&1 &

case "$1" in
	start)
	  echo "Starting capturing image"
	  ;;
	stop)
	  echo "Stopping capturing image"
	  killall raspistill
	  exit 1
	  ;;
esac

exit 0
