#!/bin/bash

xhost +

docker run -ti \
  --device=/dev/dri:/dev/dri \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  --privileged \
  -v $HOME/shared:/home/ow/shared:rw \
  openworm-nvidia:0.1 \
  /bin/bash
