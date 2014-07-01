#!/bin/sh

sleep 3
# set ubuntu computer to the proper resolution and frame rate
xrandr --output DVI-1 --primary
#xrandr -s 640x480 -r 60
sleep 2
xrandr -r 60

# install requirements
# sudo apt-get install vlc vlc-plugin-pulse mozilla-plugin-vlc
# sudo apt-get update
# man vlc
# vlc --help
# vlc --fullscreen "/home/tkachlab/Desktop/run0.avi"

sleep 3
#echo -n m > /dev/ttyS0
# send start command to the ardunio
echo -n z > /dev/ttyACM0

# necessary fiddling
echo "to get projector working: turn off, unplug, turn on, replug"




