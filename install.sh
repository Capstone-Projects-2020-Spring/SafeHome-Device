sudo apt-get install -y git \
libgstreamer1.0-0 \
gstreamer1.0-plugins-base \
gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad \
gstreamer1.0-plugins-ugly \
gstreamer1.0-libav \
gstreamer1.0-doc \
gstreamer1.0-tools \
gstreamer1.0-x \
gstreamer1.0-alsa \
gstreamer1.0-gl \
gstreamer1.0-gtk3 \
autoconf \
automake \
libtool \
pkg-config \
libgstreamer1.0-dev \
libgstreamer-plugins-base1.0-dev \
libraspberrypi-dev \
nginx \
libi2c-dev \
libavutil-dev \
lib avcodec-dev \
libavformat-dev
sudo apt install -y libnginx-mod-rtmp
sudo raspi-config nonint do_camera 1
sudo git clone https://github.com/thaytan/gst-rpicamsrc
cd gst-rpicamsrc
sudo ./autogen.sh
sudo make
sudo make install
cd ..
git clone https://github.com/pimoroni/mlx90640-library.git
cd mlx90640-library
sudo wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.55.tar.gz
tar xvfz bcm2835-1.63.tar.gz
cd bcm2835-1.63
./configure
make
sudo make install
cd ..
sudo make I2C_MODE=RPI I2C_LIBS = -lbcm2835
sudo make install
cd ..
sudo cat /etc/nginx/nginx.conf rtmp_nginx.conf > /etc/nginx/nginx.conf
sudo systemctl restart nginx
