#!/bin/bash

OW_OUT_DIR=/home/ow/shared

xhost +

docker run -ti \
  --device /dev/nvidia0:/dev/nvidia0 \
  --device /dev/nvidiactl:/dev/nvidiactl \
  --device /dev/nvidia-uvm:/dev/nvidia-uvm \
  -e DISPLAY=$DISPLAY \
  -e OW_OUT_DIR=$OW_OUT_DIR \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $HOME/shared:$OW_OUT_DIR:rw \
  openworm-nvidia:0.1 \
  /bin/bash
