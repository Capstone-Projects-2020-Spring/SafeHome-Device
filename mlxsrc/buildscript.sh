g++ -Wall -Werror -fPIC $CPPFLAGS $(pkg-config --cflags gstreamer-1.0 gstreamer-base-1.0) -c -o rawrgb.o rawrgb.cpp


g++ -shared -o rawrgb.so rawrgb.o $(pkg-config --libs gstreamer-1.0 gstreamer-base-1.0)


#gst-inspect-1.0 ./gstmlxsrc.so
