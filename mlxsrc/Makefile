#
# In order to execute this "Makefile" just type "make"
#	A. Delis (ad@di.uoa.gr)
#

OBJS	= rawrgb.o
SOURCE	= rawrgb.cpp
HEADER	= 
OUT	= rawrgb
CC	 = g++
FLAGS	 = -g -c -Wall
LFLAGS	 = -lpthread -lbcm2835 -lMLX90640 -lcurl
# -g option enables debugging mode 
# -c flag generates object code for separate files


all: $(OBJS)
	$(CC) -g $(OBJS) -o $(OUT) $(LFLAGS)


# create/compile the individual files >>separately<<
rawrgb.o: rawrgb.cpp
	$(CC) $(FLAGS) rawrgb.cpp -std=c++11


# clean house
clean:
	rm -f $(OBJS) $(OUT)
