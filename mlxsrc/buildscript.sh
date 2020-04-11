gcc -Wall -Werror -fPIC $CPPFLAGS $(pkg-config --cflags gstreamer-1.0 gstreamer-base-1.0) -c -o gstmlxsrc.o gstmlxsrc.c


gcc -shared -o gstmlxsrc.so gstmlxsrc.o $(pkg-config --libs gstreamer-1.0 gstreamer-base-1.0)


gst-inspect-1.0 ./gstmlxsrc.so
