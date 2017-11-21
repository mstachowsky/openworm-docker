#!/bin/bash

xhost +

docker run -ti \
  --device /dev/nvidia0:/dev/nvidia0 \
  --device /dev/nvidiactl:/dev/nvidiactl \
  --device /dev/nvidia-uvm:/dev/nvidia-uvm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $HOME/shared:/home/ow/shared:rw \
  openworm-nvidia:0.1 \
  /bin/bash
