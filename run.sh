#!/bin/bash

OW_OUT_DIR=/home/ow/shared

xhost +

docker run -d \
  --name openworm \
  --device=/dev/dri:/dev/dri \
  -e DISPLAY=$DISPLAY \
  -e OW_OUT_DIR=$OW_OUT_DIR \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --privileged \
  -v $HOME/shared:$OW_OUT_DIR:rw \
  openworm/openworm:0.7 \
  DISPLAY=:44 python master_openworm.py
